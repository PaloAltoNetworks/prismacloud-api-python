""" Import Account Groups from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility
import numpy as np
import json

# --Configuration-- #

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

# --Main-- #

## --Create Role-- ##

print('API - Getting the current updated list of Account Groups ...', end='')
cloud_account_group_list_updated = pc_api.cloud_account_group_list_read()
print(' done.')
print()

cloud_roles_to_create = []
for cloud_account_group in cloud_account_group_list_updated:
    if cloud_account_group['name'].lower()[0:len(args.prefix)] == args.prefix:
        cloud_role = {}
        cloud_role['name'] = cloud_account_group['name'].lower().replace(args.prefix,"role_")
        cloud_role['roleType'] = "wistron-read-only"
        cloud_role['accountGroupIds'] = [cloud_account_group['id']]
        cloud_roles_to_create.append(cloud_role)

print('API - Creating Roles ...')
for cloud_role_to_create in cloud_roles_to_create:
    print('Adding Roles: %s' % cloud_role_to_create['name'])
    pc_api.user_role_create(cloud_role_to_create)
print()
