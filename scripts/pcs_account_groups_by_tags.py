"""
pcs_account_groups_by_tags.py: using cloud provider tags applied to cloud accounts to automatically place them into Prisma Cloud account groups
"""

import json

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
    '--export_file_name',
    type=str,
    help='(Optionl) Export file name for the Resources.')
parser.add_argument(
    '--key',
    type=str,
    default="owner",
    help='Cloud tag to assign by')
parser.add_argument(
    '--save',
    type=str,
    help='(Optional) Save cloud account data')

args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

aws_rql = "config from cloud.resource where api.name = 'aws-organizations-account'"
azure_rql = "config from cloud.resource where cloud.service = 'Azure Subscriptions'"
gcloud_rql = "config from cloud.resource where api.name = 'gcloud-compute-project-info'"

search_params = {'query': aws_rql}
aws_accounts = pc_api.search_config_read(search_params)
if args.save:
    print('Saving data to %s' % (args.save))
    with open(args.save, 'w') as outfile:
        outfile.write(json.dumps(aws_accounts, indent=3))

# Get AWS accounts and save correctly tagged accounts

tagged_accounts = []
print('Key tag: %s' % (args.key))
print('%d accounts found' % (len(aws_accounts)))
print('Tagged accounts')
for account in aws_accounts:
    account_data = account['data']
    for tag in account_data['tags']:
        if tag['key'] == args.key:
            tagged_accounts.append(account_data)
            print('   %s: %s' % (account_data['name'], tag['value']))
