from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general
import json


# --Execution Block-- #
# --Parse command line arguments-- #
parser = pc_lib_general.pc_arg_parser_defaults()

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

# Get policy list
print('API - Getting the policy list...', end='')
pc_settings, response_package = pc_lib_api.api_policy_list_get(pc_settings)
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
    pc_lib_general.pc_exit_error(500, 'Entered Policy Name was not found!')
print('Done.')

# Print the JSON object from the policy list API call (different from the specific policy object call below)
print()
print('Policy from list:')
print(json.dumps(policy))
print()

# Get the individual complete policy object from the API
print('API - Getting the specific policy...', end='')
pc_settings, response_package = pc_lib_api.api_policy_get(pc_settings, policy_id)
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
    pc_settings, response_package = pc_lib_api.api_search_get(pc_settings, policy['rule']['criteria'])
    policy_search = response_package['data']

    # Print the search object for the policy
    print()
    print('Related Saved Search Object:')
    print(json.dumps(policy_search))
