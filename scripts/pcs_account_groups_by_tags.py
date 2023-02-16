"""
Use cloud provider tags applied to cloud accounts to automatically place them into Prisma Cloud Account Groups.
"""


# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--cloud_provider',
    type=str,
    choices=['aws', 'azure', 'gcp'],
    default='aws',
    help='Cloud Provider.')
parser.add_argument(
    '--key',
    type=str,
    default='owner',
    help='Tag Key to use to assign Cloud Account Groups.')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Helpers --#

def summarize_account_groups(groups):
    results = {}
    for group in groups:
        if 'description' not in group:
            account_group['description'] = ''
        results[groups['name']] = {
            'id':          group['id'],
            'name':        group['name'],
            'description': group['description'],
            'accountIds':  group['accountIds']
        }
    return results

# --Main-- #

# Only RQL returns cloud account tags.
# But there is no guarantee that all accounts returned by RQL have been onboarded.
#
# TODO: Merge the Cloud Accounts endpoints results (including parents) with RQL results.
#       Use those IDs to create or update Cloud Account Groups.

aws_rql   = "config from cloud.resource where api.name = 'aws-organizations-account'"
azure_rql = "config from cloud.resource where cloud.service = 'Azure Subscriptions'"
gcp_rql   = "config from cloud.resource where api.name = 'gcloud-compute-project-info'"

if args.cloud_provider == 'aws':
    search_params = {'query': aws_rql}
if args.cloud_provider == 'azure':
    search_params = {'query': azure_rql}
if args.cloud_provider == 'gcp':
    search_params = {'query': gcp_rql}

print('Using Tag Key: %s' % (args.key))
print()

print('Reading Cloud Accounts')
cloud_accounts = pc_api.search_config_read(search_params)
print('%d Cloud Accounts Found' % len(cloud_accounts))
print()

print('Reading Cloud Account Groups')
account_groups = pc_api.cloud_account_group_list_read()
print('%d Cloud Account Groups Found' % len(account_groups))
print()

account_groups = summarize_account_groups(account_groups)

print('Matching Cloud Accounts:')
print()
for cloud_account in cloud_accounts:
    account_data = cloud_account['data']
    for tag in account_data['tags']:
        if tag['key'] == args.key:
            if tag['value'] in account_groups:
                account_group = account_groups[tag['value']]
                if cloud_account['id'] not in account_group['accountIds']:
                    print('Adding Cloud Account (%s) to Cloud Account Group (%s)' % (account_data['name'], account_group['name']))
                    account_group['accountIds'].append(cloud_account['id'])
                    payload = {
                        'name':        account_group['name'],
                        'description': account_group['description'],
                        'accountIds':  account_group['accountIds']
                    }
                    result = pc_api.cloud_account_group_update(account_group['id'], payload)
                    print(result)
            else:
                print('Creating Cloud Account Group (%s) and adding Cloud Account (%s)' % (tag['value'], account_data['name']))
                payload = {
                    'name':        tag['value'],
                    'description': account_group['description'],
                    'accountIds':  [cloud_account['id']]
                }
                result = pc_api.cloud_account_group_create(payload)
                print(result)
                account_groups[tag['value']] = {
                   'id':          result['id'],
                   'name':        result['name'],
                   'description': result['description'],
                   'accountIds':  result['accountIds']
                }

"""
[{
	'id': '1234-5678-1234-5678-12345678',
	'name': 'TJKCloudAccounts',
	'description': '',
	'accountIds': ['1234567890'],
	'nonOnboardedCloudAccountIds': [],
	'autoCreated': False,
	'accounts': [{
		'id': '1234567890',
		'name': 'TJK - AWS Account',
		'type': 'aws'
	}]
}]
"""
