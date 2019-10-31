from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import rl_lib_api
import rl_lib_general


# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required* - Prisma Cloud API Access Key ID that you want to set to access your Prisma Cloud account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required* - Prisma Cloud API Secret Key that you want to set to access your Prisma Cloud account.')

parser.add_argument(
    '-url',
    '--uiurl',
    type=str,
    help='*Required* - Base URL used in the UI for connecting to Prisma Cloud.  '
         'Formatted as app.prismacloud.io or app2.prismacloud.io or app.eu.prismacloud.io, etc.  '
         'You can also input the api version of the URL if you know it and it will be passed through.')

parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='(Optional) - Override user input for verification (auto answer for yes).')

parser.add_argument(
    'source_csv_cloud_accounts_list',
    type=str,
    help='Filename of the file with the list of cloud accounts to import (CSV).')


args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
rl_settings = rl_lib_general.rl_login_get(args.username, args.password, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to excute commands aginst your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        rl_lib_general.rl_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
rl_settings = rl_lib_api.rl_jwt_get(rl_settings)
print('Done.')

# Ingest CSV list of accounts to add
print('File - Importing CSV from disk...', end='')
import_list_from_csv = rl_lib_general.rl_file_load_csv(args.source_csv_cloud_accounts_list)
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
        rl_lib_general.rl_exit_error(400, 'monitorFlowLogs value did not appear to be true or false.  Only true or false is recognized as an input value in the CSV.')

    if cloud_account['enabled'].lower() == "true":
        cloud_account['enabled'] = True
    elif cloud_account['enabled'].lower() == "false":
        cloud_account['enabled'] = False
    else:
        rl_lib_general.rl_exit_error(400, 'enabled value did not appear to be true or false.  Only true or false is recognized as an input value in the CSV.')

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
rl_settings, response_package = rl_lib_api.api_cloud_accounts_list_get(rl_settings)
cloud_accounts_list = response_package['data']
print('Done.')

# Figure out which accounts are already in Redlock and remove them from the import list
## To Do ##

# Check the remaining list for any duplicate names
## To Do ##

# Import the account list into Redlock
print('API - Adding cloud accounts...')
cloud_type = "azure"
print()
for new_cloud_account in cloud_accounts_to_import:
    print('Adding cloud account: ' + new_cloud_account['cloudAccount']['name'])
    rl_settings, response_package = rl_lib_api.api_cloud_accounts_add(rl_settings, cloud_type, new_cloud_account)

print()
print('Import Complete.')
