""" Import Account Groups from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility
import numpy as np
import json

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import (CSV) file name for the Account Groups.')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Getting the current list of Account Groups ...', end='')
cloud_account_group_list_current = pc_api.cloud_account_group_list_read()
print(' done.')
print()

## --Create User-- #

cloud_account_group_list_to_import = pc_utility.read_csv_file_text(args.import_file_name)
cloud_roles_updated = pc_api.user_role_list_read()
user_list_current = pc_api.user_list_read()
users_to_import = []


print('API - Getting the current Prisma Cloud user list ...', end='')
print()

for user_to_create in cloud_account_group_list_to_import:
    user_roles_update = []
    for user_current in user_list_current:
        user = {}
        if user_to_create['username'].lower() == user_current['email'].lower():
            print('Existing User found with email: %s' % user_to_create['username'].lower())
            #print('Existing User Roles: %s' % user_current['roleIds'])
            #print('Existing User Default Role: %s' % user_current['defaultRoleId'])
            for cloud_role in cloud_roles_updated:
                if user_to_create['username'].lower() in cloud_role['name']:
                    if cloud_role['id'] in user_current['roleIds']: 
                        print('Role Already Mapped to User, No Action Required')
                    else:
                        user_roles_update = user_current['roleIds']
                        user_roles_update += [cloud_role['id']]
                        user = user_current
                        user['roleIds'] = user_roles_update
                        pc_api.user_update(user)
                        print('User Roles Updated with: %s' % user['roleIds'])
                    break
            break

print('done.')
print()


