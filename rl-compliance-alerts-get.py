from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import rl_lib_api
import rl_lib_general
import json


# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required if no settings file has been created* - Redlock API UserName that you want to set to access your Redlock account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required if no settings file has been created* - Redlock API password that you want to set to access your Redlock account.')

parser.add_argument(
    '-c',
    '--customername',
    type=str,
    help='*Required if no settings file has been created* - Name of the Redlock account to be used.')

parser.add_argument(
    '-url',
    '--uiurl',
    type=str,
    help='*Required if no settings file has been created* - Base URL used in the UI for connecting to Redlock.  '
         'Formatted as app.redlock.io or app2.redlock.io or app.eu.redlock.io, etc.')

parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='(Optional) - Override user input for verification (auto answer for yes).')

parser.add_argument(
    'source_compliance_standard_name',
    type=str,
    help='Name of the compliance standard to filter on.  Please enter it exactly as listed in the Redlock UI')

parser.add_argument(
    'source_cloud_account_name',
    type=str,
    help='Name of the cloud account to filter on.  Please enter it exactly as listed in the Redlock UI')


args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
rl_settings = rl_lib_general.rl_login_get(args.username, args.password, args.customername, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('This action will be done against the customer account name of "' + rl_settings['customerName'] + '".')
    verification_response = str(input('Is this correct (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        rl_lib_general.rl_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
rl_settings = rl_lib_api.rl_jwt_get(rl_settings)
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
rl_settings, response_package = rl_lib_api.api_compliance_standard_policy_list_get(rl_settings, compliance_standard_name)
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
    rl_settings, response_package = rl_lib_api.api_alert_list_get(rl_settings, data=alert_filter)
    alert_list_complete.extend(response_package['data'])
    print('Done.')

# Print the resulting data to the console
print()
print(json.dumps(alert_list_complete))
