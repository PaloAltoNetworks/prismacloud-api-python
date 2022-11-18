""" Get Resources """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--cloud_account_name',
    type=str,
    help='Name of the Cloud Account to get Resources.')
parser.add_argument(
    '--concurrency',
    type=int,
    default=0,
    help='(Optional) - Number of concurrent API calls. (1-16)')
parser.add_argument(
    'export_file_name',
    type=str,
    help='Export file name for the Resources.')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Getting the current list of Cloud Accounts ...', end='')
cloud_accounts_list = pc_api.cloud_accounts_list_read(query_params={'excludeAccountGroupDetails': 'true'})
print(' done.')
print()

# Optionally filter the list of cloud accounts down to the one specified on the command line.
if args.cloud_account_name:
    cloud_accounts_list = [next(item for item in cloud_accounts_list if item['name'] == args.cloud_account_name)]

# Avoid API rate limits.
if args.concurrency > 0 and args.concurrency <= 16:
    pc_api.max_workers = args.concurrency
print('Limiting concurrent API calls to: (%s)' % pc_api.max_workers)
print()

resource_list = []

for cloud_account in cloud_accounts_list:
    body_params = {
        'filters':[
            {'operator':'=', 'name':'includeEventForeignEntities', 'value': 'false'},
            {'operator':'=', 'name':'asset.severity', 'value': 'all'},
            {'operator':'=', 'name':'cloud.account',  'value': '%s' % cloud_account['name']},
            {'operator':'=', 'name':'cloud.type',     'value': '%s' % cloud_account['deploymentType']},
            {'operator':'=', 'name':'scan.status',    'value': 'all'}],
        'limit': 1000,
        'timeRange': {'type': 'to_now'}
    }
    print('API - Getting the current Resources for Cloud Account: %s ...' % cloud_account['name'])
    cloud_account_resource_list = pc_api.resource_scan_info_read(body_params=body_params)
    print('Done.')
    # Threaded Queries.
    resource_list.append(pc_api.get_cloud_resources(cloud_account_resource_list))

pc_utility.write_json_file(args.export_file_name, resource_list)
print()
print('Exported to: %s' % args.export_file_name)

pc_api.error_report()
