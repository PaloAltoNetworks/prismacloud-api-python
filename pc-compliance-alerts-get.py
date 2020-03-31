from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import pc_lib_api
import pc_lib_general
import json


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
    'source_compliance_standard_name',
    type=str,
    help='Name of the compliance standard to filter on.  Please enter it exactly as listed in the Prisma Cloud UI')

parser.add_argument(
    'source_cloud_account_name',
    type=str,
    help='Name of the cloud account to filter on.  Please enter it exactly as listed in the Prisma Cloud UI')


args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to excute commands aginst your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        pc_lib_general.pc_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print('Done.')

# Get the standard and cloud account name from the command line
compliance_standard_name = args.source_compliance_standard_name
cloud_account_name = args.source_cloud_account_name

# Set some values used in the filter
alert_status = "open"
alert_detail = True
timeRange_type = "to_now"
timeRange_value = "epoch"

# Get the Policies list for the Compliance Standard
print('API - Getting the compliance standard policy list...', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_policy_list_get(pc_settings, compliance_standard_name)
compliance_policy_list = response_package['data']
print('Done.')

# Loop through the policy list to collect the related alerts for a given cloud account
alert_list_complete = []
for compliance_policy in compliance_policy_list:
    alert_filter = {"detailed": alert_detail,
                    "timeRange": {"type": timeRange_type, "value": timeRange_value},
                    "filters": [{"operator": "=", "name": "alert.status", "value": alert_status},
                                {"operator": "=", "name": "cloud.account", "value": cloud_account_name},
                                {"name": "policy.id", "operator": "=", "value": compliance_policy['policyId']}]
                   }

    print('API - Getting the alerts for the policy named: ' + compliance_policy['name'] + '...', end='')
    pc_settings, response_package = pc_lib_api.api_alert_list_get(pc_settings, data=alert_filter)
    alert_list_complete.extend(response_package['data'])
    print('Done.')

# Print the resulting data to the console
print()
print(json.dumps(alert_list_complete))
