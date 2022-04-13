""" Get a Policy """

import json

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
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

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Get Policy

print('API - Getting the Policy list ...', end='')
policy_list = pc_api.policy_list_read()
print(' done.')
print()

# TODO: Replace with library function.

policy_id = None
for policy in policy_list:
    if policy['name'].lower() == args.policy_name.lower():
        policy_id = policy['policyId']
        break
if policy_id is None:
    pc_utility.error_and_exit(500, 'Policy was not found. Please verify the Policy name.')

print()
print('Policy from Policy list:')
print(policy_id)
print()

print('API - Getting the Policy ...', end='')
policy = pc_api.policy_read(policy_id)
print(' done.')
print()

print('Policy:')
print(json.dumps(policy))
print()

if args.rql:
    print('API - Getting the RQL (Saved Search) ...', end='')
    policy_search = pc_api.saved_search_read(policy['rule']['criteria'])
    print(' done.')
    print()

    print('RQL (Saved Search):')
    print(json.dumps(policy_search))
    print()
