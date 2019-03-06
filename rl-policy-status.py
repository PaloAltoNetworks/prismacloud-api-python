from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import rl_lib_general
import rl_lib_api


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
    'policytype',
    type=str,
    choices=['config', 'network', 'audit_event', 'anomaly', 'all'],
    help='Policy type to enable/disable.')

parser.add_argument(
    'status',
    type=str,
    choices=['enable', 'disable'],
    help='Policy status to change the policy types to (enable or disable).')

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

print('API - Getting list of Policies...', end='')
rl_settings, response_package = rl_lib_api.api_policy_list_get(rl_settings)
policy_list_old = response_package['data']
print('Done.')

print('Filter policy list for indicated policy types of ' + args.policytype + '...', end='')
policy_type = args.policytype.lower()
policy_list_filtered = []

if args.status.lower() == "enable":
    policy_enabled = True
    policy_enabled_str = "true"
else:
    policy_enabled = False
    policy_enabled_str = "false"

for policy_old in policy_list_old:
    if policy_old['enabled'] is not policy_enabled:
        if policy_type == "all":
            policy_list_filtered.append(policy_old)
        elif policy_old['policyType'] == policy_type:
            policy_list_filtered.append(policy_old)
print('Done.')

print('API - Updating policy statuses...')
for policy_update in policy_list_filtered:
    print('Updating policy: ' + policy_update['name'])
    rl_settings, response_package = rl_lib_api.api_policy_status_update(rl_settings, policy_update['policyId'], policy_enabled_str)
print('Done.')
