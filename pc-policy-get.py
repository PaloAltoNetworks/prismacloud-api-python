from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
from pc_lib_api import pc_api
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

# --Initialize-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)
pc_settings = pc_lib_general.pc_settings_get(args.username, args.password, args.uiurl, args.config_file)
pc_api.configure(pc_settings['apiBase'], pc_settings['username'], pc_settings['password'])

# --Main-- #

# Get Policy

print('API - Getting the Policy list ...', end='')
policy_list = pc_lib_api.api_policy_list_get()
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
policy = pc_lib_api.api_policy_get(policy_id)
print(' done.')
print()

print('Policy:')
print(json.dumps(policy))
print()

if args.rql:
    print('API - Getting the RQL (Saved Search) ...', end='')
    policy_search = pc_lib_api.api_search_get(policy['rule']['criteria'])
    print(' done.')
    print()

    print('RQL (Saved Search):')
    print(json.dumps(policy_search))
    print()
