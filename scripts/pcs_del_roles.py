""" Import Account Groups from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility
import numpy as np
import json

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'prefix',
    type=str,
    help='The prefix of role')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)
prefix_length=len(args.prefix)

# --Main-- #

print('API - Getting the current list of roles ...', end='')
role_list_current = pc_api.user_role_list_read()
print(' done.')
print()

## --Delete User-- #

users_to_delete = []

for role_current in role_list_current:
    if role_current['name'][0:prefix_length] == args.prefix:
        print('Deleting role found with name: %s' % role_current['name'].lower())
        pc_api.user_role_delete(role_current['id'])

print('done.')
print()


