""" Import Account Groups from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility
import numpy as np
import json

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'prefix',
    type=str,
    help='The prefix of account group')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)
prefix_length=len(args.prefix)

# --Main-- #

print('API - Getting the current list of Users ...', end='')
cloud_user_list_current = pc_api.user_list_read()
print(' done.')
print()

## --Delete User-- #

users_to_delete = []

for user_current in cloud_user_list_current:
    if user_current['email'].lower()[prefix_length*-1:] == args.prefix:
        print('Deleting User found with email: %s' % user_current['email'].lower())
        pc_api.user_delete(user_current['email'])

print('done.')
print()


