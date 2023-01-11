"""
Use cloud provider tags applied to cloud accounts to automatically place them into Prisma Cloud Account Groups.
"""

import json

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
    default="owner",
    help='Tag Key to use to assign Account Groups.')
parser.add_argument(
    '--export_file_name',
    type=str,
    help='(Optional) Export file name for the list of Cloud Accounts.')

args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

aws_rql   = "config from cloud.resource where api.name = 'aws-organizations-account'"
azure_rql = "config from cloud.resource where cloud.service = 'Azure Subscriptions'"
gcp_rql   = "config from cloud.resource where api.name = 'gcloud-compute-project-info'"

if args.cloud_provider == 'aws':
    search_params = {'query': aws_rql}
if args.cloud_provider == 'azure':
    search_params = {'query': azure_rql}
if args.cloud_provider == 'gcp':
    search_params = {'query': gcp_rql}

accounts = pc_api.search_config_read(search_params)
if args.export_file_name:
    print('Saving the list of Cloud Accounts to: %s' % (args.export_file_name))
    with open(args.export_file_name, 'w') as outfile:
        outfile.write(json.dumps(accounts, indent=3))

print('TO-DO: Create Account Group (args.key) if it does not exist')

print('%d Cloud Accounts Found' % (len(accounts)))
print('Tag Key: %s' % (args.key))

print('Matching Cloud Accounts:')
print()
for account in accounts:
    account_data = account['data']
    for tag in account_data['tags']:
        if tag['key'] == args.key:
            print('%s: %s' % (account_data['name'], tag['value']))
            print('TO-DO: Add this Account to Account Group (args.key)')
