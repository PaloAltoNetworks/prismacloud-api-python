from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general


# --Execution Block-- #
# --Parse command line arguments-- #
parser = pc_lib_general.pc_arg_parser_defaults()

parser.add_argument(
    'source_csv_cloud_accounts_list',
    type=str,
    help='Filename of the file with the list of cloud accounts to import (CSV).')


args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to execute commands against your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        pc_lib_general.pc_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print('Done.')

# Ingest CSV list of accounts to add
print('File - Importing CSV from disk...', end='')
import_list_from_csv = pc_lib_general.pc_file_load_csv(args.source_csv_cloud_accounts_list)
print('Done.')

# Convert groupId to an array for import
print('Data - Converting CSV data format for import...', end='')
cloud_accounts_to_import = []
for cloud_account in import_list_from_csv:
    if cloud_account['monitorFlowLogs'].lower() == "true":
        cloud_account['monitorFlowLogs'] = True
    elif cloud_account['monitorFlowLogs'].lower() == "false":
        cloud_account['monitorFlowLogs'] = False
    else:
        pc_lib_general.pc_exit_error(400, 'monitorFlowLogs value did not appear to be true or false.  Only true or false is recognized as an input value in the CSV.')

    if cloud_account['enabled'].lower() == "true":
        cloud_account['enabled'] = True
    elif cloud_account['enabled'].lower() == "false":
        cloud_account['enabled'] = False
    else:
        pc_lib_general.pc_exit_error(400, 'enabled value did not appear to be true or false.  Only true or false is recognized as an input value in the CSV.')

    temp_cloud_account = {}
    temp_cloud_account['cloudAccount'] = {}
    temp_cloud_account['cloudAccount']['accountId'] = cloud_account['accountId']
    temp_cloud_account['cloudAccount']['enabled'] = cloud_account['enabled']
    temp_cloud_account['cloudAccount']['groupIds'] = []
    temp_cloud_account['cloudAccount']['groupIds'].append(cloud_account['groupIds'])
    temp_cloud_account['cloudAccount']['name'] = cloud_account['name']
    temp_cloud_account['clientId'] = cloud_account['clientId']
    temp_cloud_account['key'] = cloud_account['key']
    temp_cloud_account['monitorFlowLogs'] = cloud_account['monitorFlowLogs']
    temp_cloud_account['tenantId'] = cloud_account['tenantId']
    temp_cloud_account['servicePrincipalId'] = cloud_account['servicePrincipalId']

    cloud_accounts_to_import.append(temp_cloud_account)
print('Done.')

# Check ingested list for all required fields and data in all fields
## To Do ##

# Check ingested list for any duplicates in the CSV (Names or account ID's)
## To Do ##

# Get existing cloud account list
print('API - Getting existing cloud account list...', end='')
pc_settings, response_package = pc_lib_api.api_cloud_accounts_list_get(pc_settings)
cloud_accounts_list = response_package['data']
print('Done.')

# Figure out which accounts are already in Prisma Cloud and remove them from the import list
## To Do ##

# Check the remaining list for any duplicate names
## To Do ##

# Import the account list into Prisma Cloud
print('API - Adding cloud accounts...')
cloud_type = "azure"
print()
for new_cloud_account in cloud_accounts_to_import:
    print('Adding cloud account: ' + new_cloud_account['cloudAccount']['name'])
    pc_settings, response_package = pc_lib_api.api_cloud_accounts_add(pc_settings, cloud_type, new_cloud_account)

print()
print('Import Complete.')
