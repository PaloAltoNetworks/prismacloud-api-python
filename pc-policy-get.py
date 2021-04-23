from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general
import json

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    '-rql',
    '--rql',
    action='store_true',
    help='(Optional) - Output the RQL (Saved Search) of the Policy.')
parser.add_argument(
    'policy_name',
    type=str,
    help='(Required) - Name of the Policy.')
args = parser.parse_args()

# --Main-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)

print('API - Getting login ...', end='')
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print(' done.')
print()

# Get Policy

print('API - Getting the Policy list ...', end='')
pc_settings, response_package = pc_lib_api.api_policy_list_get(pc_settings)
policy_list = response_package['data']
print(' done.')
print()

# TODO: Replace with library function.

policy_id = None
for policy in policy_list:
    if policy['name'].lower() == args.policy_name.lower():
        policy_id = policy['policyId']
        break
if policy_id is None:
    pc_lib_general.pc_exit_error(500, 'Policy was not found. Please verify the Policy name.')

print()
print('Policy from Policy list:')
print(json.dumps(policy))
print()

print('API - Getting the Policy ...', end='')
pc_settings, response_package = pc_lib_api.api_policy_get(pc_settings, policy_id)
policy = response_package['data']
print(' done.')
print()

print('Policy:')
print(json.dumps(policy))
print()

if args.rql:
    print('API - Getting the RQL (Saved Search) ...', end='')
    pc_settings, response_package = pc_lib_api.api_search_get(pc_settings, policy['rule']['criteria'])
    policy_search = response_package['data']
    print(' done.')
    print()

    print('RQL (Saved Search):')
    print(json.dumps(policy_search))
    print()
