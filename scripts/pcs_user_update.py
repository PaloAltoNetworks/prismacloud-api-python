""" Update a User """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'user_email',
    type=str,
    help='Email address of the User to update.')
parser.add_argument(
    '-fn',
    '--firstname',
    type=str,
    help='(Optional) - New First Name for the specified User.')
parser.add_argument(
    '-ln',
    '--lastname',
    type=str,
    help='(Optional) - New Last Name for the specified User.')
parser.add_argument(
    '-rn',
    '--role_name',
    type=str,
    help='(Optional) - New Role to assign for the specified User.')
parser.add_argument(
    '--access_keys_allowed',
    choices=['true', 'false', None],
    type=str,
    help='(Optional) - Whether Access Keys are allowed for the specified User.')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Getting the User ...', end='')
user = pc_api.user_read(args.user_email.lower())
print(' done.')
print()

update_needed = False

if args.role_name is not None:
    print('API - Getting the Roles list ...', end='')
    user_role_list = pc_api.user_role_list_read()
    print(' done.')
    print()
    user_role_id = None
    for user_role in user_role_list:
        if user_role['name'].lower() == args.role_name.lower():
            user_role_id = user_role['id']
            update_needed = True
            break
    if user_role_id is None:
        pc_utility.error_and_exit(400, 'Role not found. Please verify the Role name.')
    user['roleId'] = user_role_id

if args.firstname is not None:
    update_needed = True
    user['firstName'] = args.firstname

if args.lastname is not None:
    update_needed = True
    user['lastName'] = args.lastname

if args.access_keys_allowed is not None:
    update_needed = True
    user['accessKeysAllowed'] = args.access_keys_allowed

if update_needed:
    print('API - Updating the User ...', end='')
    pc_api.user_update(user)
    print(' done.')
    print()
else:
    print('No update required: current User attributes match new attributes.')
