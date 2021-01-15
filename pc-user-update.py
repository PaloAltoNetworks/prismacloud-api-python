from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general


# --Execution Block-- #
# --Parse command line arguments-- #
parser = pc_lib_general.pc_arg_parser_defaults()

parser.add_argument(
    'useremail',
    type=str,
    help='E-mail address for the user to update.')

parser.add_argument(
    '-fn',
    '--firstname',
    type=str,
    help='(Optional) - New First Name for the specified user.')

parser.add_argument(
    '-ln',
    '--lastname',
    type=str,
    help='(Optional) - New Last Name for the specified user.')

parser.add_argument(
    '-r',
    '--role',
    type=str,
    help='(Optional) - New Role for the specified user.')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to execute commands against your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        pc_lib_general.pc_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print('Done.')

print('API - Getting user...', end='')
pc_settings, response_package = pc_lib_api.api_user_get(pc_settings, args.useremail.lower())
user_new = response_package['data']
print('Done.')

# Figure out what was updated and then post the changes as a complete package
if args.role is not None:
    print('API - Getting user roles list...', end='')
    pc_settings, response_package = pc_lib_api.api_user_role_list_get(pc_settings)
    user_role_list = response_package['data']
    print('Done.')

    print('Searching for role name to get role ID...', end='')
    update_needed = False
    for user_role in user_role_list:
        if user_role['name'].lower() == args.role.lower():
            user_new['roleId'] = user_role['id']
            update_needed = True
            break
    if update_needed is False:
        pc_lib_general.pc_exit_error(400, 'No role by that name found.  Please check the role name and try again.')
    print('Done.')
if args.firstname is not None:
    user_new['firstName'] = args.firstname
if args.lastname is not None:
    user_new['lastName'] = args.lastname

print('API - Updating user...', end='')
pc_settings, response_package = pc_lib_api.api_user_update(pc_settings, user_new)
print('Done.')
