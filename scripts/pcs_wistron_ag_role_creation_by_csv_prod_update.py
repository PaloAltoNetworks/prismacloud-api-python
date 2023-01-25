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

print('API - Getting the current list of Account Groups ...', end='')
cloud_account_group_list_current = pc_api.cloud_account_group_list_read()
print(' done.')
print()

cloud_account_group_list_to_import = pc_utility.read_csv_file_text(args.import_file_name)

cloud_account_groups_duplicate_current_count = 0

cloud_account_groups_to_import = []
for cloud_account_group_to_import in cloud_account_group_list_to_import:
    cloud_account_group_duplicate = False
    if not cloud_account_group_duplicate:
        # Remove duplicates based upon the current cloud_account_group list.
        for cloud_account_group_current in cloud_account_group_list_current:
            if (args.prefix + "ag_" + cloud_account_group_to_import['username'].lower() + "_" + cloud_account_group_to_import['type'].lower()) == cloud_account_group_current['name'].lower():
                cloud_account_groups_duplicate_current_count = cloud_account_groups_duplicate_current_count + 1
                cloud_account_group_duplicate = True
                cloud_account_group_id = cloud_account_group_current['id']
                break
    # if not cloud_account_group_duplicate:
    if cloud_account_group_duplicate:
        cloud_account_group = {}
        cloud_account_group['id'] = cloud_account_group_id #new added 20230115
        cloud_account_group['name'] = args.prefix + "ag_" + cloud_account_group_to_import['username'].lower() + "_" + cloud_account_group_to_import['type'].lower()
        cloud_account_group['description'] = cloud_account_group_to_import['description']
        accountId_string = cloud_account_group_to_import['accountIds'][1:-1]
        accountId_string = accountId_string.replace("'","")
        accountId_string = accountId_string.replace(" ","")
        cloud_account_group['accountIds'] = accountId_string.split(',')
        cloud_account_groups_to_import.append(cloud_account_group)
        
print('Cloud Account Groups to add: %s' % len(cloud_account_groups_to_import))
print('Cloud Account Groups skipped (duplicates in Prisma Cloud): %s' % cloud_account_groups_duplicate_current_count)

print('API - Creating Cloud Account Groups ...')
for cloud_account_group_to_import in cloud_account_groups_to_import:
    print('Adding Cloud Account Group: %s' % cloud_account_group_to_import['name'])
    # pc_api.cloud_account_group_create(cloud_account_group_to_import)
    pc_api.cloud_account_group_update(cloud_account_group_to_import['id'],cloud_account_group_to_import)
print()

## --Create Role-- ##

print('API - Getting the current updated list of Account Groups ...', end='')
cloud_account_group_list_updated = pc_api.cloud_account_group_list_read()
print(' done.')
print()

cloud_roles_to_create = []
for cloud_account_group in cloud_account_group_list_updated:
    if cloud_account_group['name'].lower()[0:len(args.prefix)] == args.prefix:
        cloud_role = {}
        cloud_role['name'] = cloud_account_group['name'].lower().replace("ag_","role_")
        cloud_role['roleType'] = "wistron-read-only"
        cloud_role['accountGroupIds'] = [cloud_account_group['id']]
        cloud_roles_to_create.append(cloud_role)

cloud_roles_updated = pc_api.user_role_list_read()

print('API - Creating Roles ...')

for cloud_role_to_create in cloud_roles_to_create:
    create_role = True
    for cloud_role in cloud_roles_updated:
        if (cloud_role['name']==cloud_role_to_create['name']):
            create_role = False
            print('Role found, skip creation')
            break
    if (create_role):    
        print('Adding Roles: %s' % cloud_role_to_create['name'])
        pc_api.user_role_create(cloud_role_to_create)
print()

cloud_roles_updated = pc_api.user_role_list_read()

## --Create User-- #

print('API - Getting the current Prisma Cloud user list ...', end='')
print()

user_list_current = pc_api.user_list_read()
for user_to_create in cloud_account_group_list_to_import:
    user_roles_update = []
    user_creation_flag = True
    for user_current in user_list_current:
        user = {}
        if user_to_create['username'].lower() == user_current['email'].lower():
            print('Existing User found with email: %s' % user_to_create['username'].lower())
            #print('Existing User Roles: %s' % user_current['roleIds'])
            #print('Existing User Default Role: %s' % user_current['defaultRoleId'])
            for cloud_role in cloud_roles_updated:
                if user_to_create['username'].lower() in cloud_role['name']:
                    user_creation_flag = False
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
    if user_creation_flag:
        print('Creating User with email: %s' % user_to_create['username'].lower())
        user = {}
        user_roles_update = []
        for cloud_role in cloud_roles_updated:
            if user_to_create['username'].lower() in cloud_role['name']:
                user_roles_update += [cloud_role['id']]
                user['roleIds'] = user_roles_update
                user['defaultRoleId'] = cloud_role['id']
        user['email']     = user_to_create['username'].lower()
        user['firstName'] = user_to_create['firstName']
        user['lastName']  = user_to_create['lastName']
        user['timeZone']  = 'America/Los_Angeles'
        pc_api.user_create(user)
        print('User Created')
        user_list_current = pc_api.user_list_read()

print('Done.')


