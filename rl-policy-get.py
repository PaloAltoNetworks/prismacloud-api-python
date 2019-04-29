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
    '-rql',
    '--rql',
    action='store_true',
    help='(Optional) - Output the related RQL (saved search) object.')

parser.add_argument(
    'policy_name',
    type=str,
    help='*Required* - Policy name to get from the API.')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
rl_settings = rl_lib_general.rl_login_get(args.username, args.password, args.customername, args.uiurl)

# Verification of account (override with -y)
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

# Get policy list
print('API - Getting the policy list...', end='')
rl_settings, response_package = rl_lib_api.api_policy_list_get(rl_settings)
policy_list = response_package['data']
print('Done.')

# Figure out the policy ID from the name entered
print('Search - Locate Policy ID from policy name...', end='')
policy_id = None
for policy in policy_list:
    if policy['name'].lower() == args.policy_name.lower():
        policy_id = policy['policyId']
        break
if policy_id is None:
    rl_lib_general.rl_exit_error(500, 'Entered Policy Name was not found!')
print('Done.')

# Print the JSON object from the policy list API call (different from the specific policy object call below)
print()
print('Policy from list:')
print(json.dumps(policy))
print()

# Get the individual complete policy object from the API
print('API - Getting the specific policy...', end='')
rl_settings, response_package = rl_lib_api.api_policy_get(rl_settings, policy_id)
policy_specific = response_package['data']
print('Done.')

# Print the JSON object from the specific policy API call (use this one for any updates to the policy object)
print()
print('Original Policy Object:')
print(json.dumps(policy_specific))
print()

# Print the JSON object of the related Saved Search (if desired with the -rql switch)
if args.rql:
    # Get the related Saved Search object for the policy
    rl_settings, response_package = rl_lib_api.api_search_get(rl_settings, policy['rule']['criteria'])
    policy_search = response_package['data']

    # Print the search object for the policy
    print()
    print('Related Saved Search Object:')
    print(json.dumps(policy_search))
