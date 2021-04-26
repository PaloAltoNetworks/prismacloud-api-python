from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import (CSV) file name for the Cloud Accounts.')
args = parser.parse_args()

# --Main-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)

print('API - Getting login ...', end='')
pc_settings = pc_lib_general.pc_settings_get(args.username, args.password, args.uiurl, args.config_file)
pc_settings = pc_lib_api.pc_login(pc_settings)
print(' done.')
print()

# Import.

import_file_data = pc_lib_general.pc_file_load_csv(args.import_file_name)

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
pc_settings, response_package = pc_lib_api.api_cloud_accounts_list_get(pc_settings)
cloud_accounts_list = response_package['data']
print(' done.')
print()

# TODO: Check list for any duplicates (in Prisma Cloud). See pc-user-import.py.

# Import the account list into Prisma Cloud
print('API - Creating Cloud Accounts ...')
cloud_type = 'azure'
for new_cloud_account in cloud_accounts_to_import:
    print('Adding Cloud Account: %s' % new_cloud_account['cloudAccount']['name'])
    pc_settings, response_package = pc_lib_api.api_cloud_accounts_add(pc_settings, cloud_type, new_cloud_account)
print('Done.')
