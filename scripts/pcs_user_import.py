""" Import Users from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import (CSV) file name for the Users.')
parser.add_argument(
    'role_name',
    type=str,
    help='Role to assign for the imported Users.')
parser.add_argument(
    '--access_keys_allowed',
    choices=['true', 'false', None],
    type=str,
    help='(Optional) - Whether Access Keys are allowed for the imported Users.')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Getting the current list of Users ...', end='')
user_list_current = pc_api.user_list_read()
print(' done.')
print()

user_list_to_import = pc_utility.read_csv_file_text(args.import_file_name)

print('API - Getting the Roles list ...', end='')
user_role_list = pc_api.user_role_list_read()
print(' done.')

user_role_id = None
for user_role in user_role_list:
    if user_role['name'].lower() == args.role_name.lower():
        user_role_id = user_role['id']
        break
if user_role_id is None:
    pc_utility.error_and_exit(400, 'Role not found. Please verify the Role name.')

users_duplicate_current_count = 0
users_duplicate_file_count = 0

users_to_import = []
for user_to_import in user_list_to_import:
    user_duplicate = False
    # Remove duplicates from the import file list.
    for user_to_import_inner in user_list_to_import:
        if user_to_import['email'].lower() == user_to_import_inner['email'].lower():
            users_duplicate_file_count = users_duplicate_file_count + 1
            user_duplicate = True
            break
    if not user_duplicate:
        # Remove duplicates based upon the current user list.
        for user_current in user_list_current:
            if user_to_import['email'].lower() == user_current['email'].lower():
                users_duplicate_current_count = users_duplicate_current_count + 1
                user_duplicate = True
                break
        if not user_duplicate:
            user = {}
            user['email']     = user_to_import['email']
            user['firstName'] = user_to_import['firstName']
            user['lastName']  = user_to_import['lastName']
            user['timeZone']  = 'America/Los_Angeles'
            user['roleId']    = user_role_id
            # TODO: Consider allowing 'roleId' in the import file to override the command line.
            # if user_to_import['roleId'] is not None:
            #     user['roleId'] = user_to_import['roleId']
            if args.access_keys_allowed is not None:
                user['accessKeysAllowed'] = args.access_keys_allowed
            # TODO: Consider allowing 'accessKeysAllowed' in the import file to override the command line.
            # if user_to_import['lastName'] is not None:
            #     user['accessKeysAllowed'] = user_to_import['accessKeysAllowed']
            users_to_import.append(user)

print('Users to add: %s' % len(users_to_import))
print('Users skipped (duplicates in Prisma Cloud): %s' % users_duplicate_current_count)
print('Users skipped (duplicates in Import File): %s' % users_duplicate_file_count)

print('API - Creating Users ...')
for user_to_import in users_to_import:
    print('Adding User: %s' % user_to_import['email'])
    pc_api.user_create(user_to_import)
print('Done.')
