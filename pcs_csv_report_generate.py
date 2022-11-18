""" Get Resources """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--severity',
    type=str,
    default='high',
    help='Alert Serverity Level, Default=High')
parser.add_argument(
    '--status',
    type=str,
    default='open',
    help='Alert Status, Default = Open')
parser.add_argument(
    '--type',
    type=str,
    default='config',
    help='Policy Type, Default = Config')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Gernerate new CSV Report ...', end='')

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
