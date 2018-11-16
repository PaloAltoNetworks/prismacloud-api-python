from __future__ import print_function
import argparse
import rl_api_lib


def api_policy_list_get(jwt):
    action = "GET"
    url = "https://api.redlock.io/policy"
    return rl_api_lib.rl_call_api(action, url, jwt=jwt)


def api_policy_status_update(jwt, policy_id, status):
    action = "PATCH"
    url = "https://api.redlock.io/policy/" + policy_id + "/status/" + status
    return rl_api_lib.rl_call_api(action, url, jwt=jwt)


# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required* - Redlock API UserName that you want to set to access your Redlock account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required* - Redlock API password that you want to set to access your Redlock account.')

parser.add_argument(
    '-c',
    '--customername',
    type=str,
    help='*Required* - Name of the Redlock account to be used.')

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
# Sort out API Login
print('API - Getting authentication token...', end='')
jwt = rl_api_lib.rl_jwt_get(args.username, args.password, args.customername)
print('Done.')

print('API - Getting list of Policies...', end='')
policy_list_old = api_policy_list_get(jwt)
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

print('API - Updating policy statuses...')
for policy_update in policy_list_filtered:
    print('Updating policy: ' + policy_update['name'])
    policy_update_response = api_policy_status_update(jwt, policy_update['policyId'], policy_enabled_str)
print('Done.')
