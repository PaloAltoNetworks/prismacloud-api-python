""" Import Azure Accounts from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import (CSV) file name for the Cloud Accounts.')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Import.

import_file_data = pc_utility.read_csv_file_text(args.import_file_name)

cloud_accounts_to_import = []
for cloud_account in import_file_data:
    if cloud_account['monitorFlowLogs'].lower() == 'true':
        cloud_account['monitorFlowLogs'] = True
    else:
        cloud_account['monitorFlowLogs'] = False
    if cloud_account['enabled'].lower() == 'true':
        cloud_account['enabled'] = True
    else:
        cloud_account['enabled'] = False
    cloud_account_new = {}
    cloud_account_new['cloudAccount'] = {}
    cloud_account_new['clientId']                  = cloud_account['clientId']
    cloud_account_new['cloudAccount']['accountId'] = cloud_account['accountId']
    cloud_account_new['cloudAccount']['enabled']   = cloud_account['enabled']
    cloud_account_new['cloudAccount']['groupIds']  = []
    cloud_account_new['cloudAccount']['groupIds'].append(cloud_account['groupIds'])
    cloud_account_new['cloudAccount']['name']      = cloud_account['name']
    cloud_account_new['key']                       = cloud_account['key']
    cloud_account_new['monitorFlowLogs']           = cloud_account['monitorFlowLogs']
    cloud_account_new['servicePrincipalId']        = cloud_account['servicePrincipalId']
    cloud_account_new['tenantId']                  = cloud_account['tenantId']
    cloud_accounts_to_import.append(cloud_account_new)

# TODO: Check list for any duplicates (in CSV). See pc-user-import.py.

print('API - Getting the current list of Cloud Accounts ...', end='')
cloud_accounts_list = pc_api.cloud_accounts_list_read()
print(' done.')
print()

# TODO: Check list for any duplicates (in Prisma Cloud). See pc-user-import.py.

# Import the account list into Prisma Cloud
print('API - Creating Cloud Accounts ...')
for cloud_account_to_import in cloud_accounts_to_import:
    print('Adding Cloud Account: %s' % cloud_account_to_import['cloudAccount']['name'])
    pc_api.cloud_accounts_create('azure', cloud_account_to_import)
print('Done.')
