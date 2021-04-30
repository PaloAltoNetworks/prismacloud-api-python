from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
from pc_lib_api import pc_api
import pc_lib_general

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
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
    '-r',
    '--role',
    type=str,
    help='(Optional) - New Role for the specified User.')
args = parser.parse_args()

# --Initialize-- #

pc_lib_general.prompt_for_verification_to_continue(args)
pc_settings = pc_lib_general.pc_settings_get(args)
pc_api.configure(pc_settings)

# --Main-- #

print('API - Getting the User ...', end='')
user = pc_api.user_get(args.user_email.lower())
print(' done.')
print()

if args.role is not None:
    print('API - Getting the Roles list ...', end='')
    role_list = pc_api.user_role_list_get()
    print(' done.')
    print()
    update_needed = False
    for role in role_list:
        if role['name'].lower() == args.role.lower():
            user['roleId'] = role['id']
            update_needed = True
            break

if args.firstname is not None:
    update_needed = True
    user['firstName'] = args.firstname

if args.lastname is not None:
    update_needed = True
    user['lastName'] = args.lastname

if update_needed:
    print('API - Updating the User ...', end='')
    pc_api.user_update(user)
    print(' done.')
    print()
else:
    print('No update required: current User attributes match new attributes.')
