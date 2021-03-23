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
    'importfile',
    type=str,
    help='File to Import from.')

parser.add_argument(
    'userrolename',
    type=str,
    help='Name of the role to assign the users for import.')

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

print('API - Getting current user list...', end='')
pc_settings, response_package = pc_lib_api.api_user_list_get(pc_settings)
user_list_old = response_package['data']
print('Done.')

print('File - Loading CSV user data...', end='')
user_list_new = pc_lib_general.pc_file_load_csv_text(args.importfile)
print('Done.')

print('API - Getting user roles...', end='')
pc_settings, response_package = pc_lib_api.api_user_role_list_get(pc_settings)
user_role_list = response_package['data']
print('Done.')

print('Searching for role name to get role ID...', end='')
user_role_id = None
for user_role in user_role_list:
    if user_role['name'].lower() == args.userrolename.lower():
        user_role_id = user_role['id']
        break
if user_role_id is None:
    pc_lib_general.pc_exit_error(400, 'No role by that name found.  Please check the role name and try again.')
print('Done.')

print('Formatting imported user list and checking for duplicates by e-mail...', end='')
users_added_count = 0
users_skipped_count = 0
users_duplicate_count = 0
users_list_new_formatted = []

for user_new in user_list_new:
    #Check for duplicates in the imported CSV
    user_exists = False
    for user_duplicate_check in users_list_new_formatted:
        if user_duplicate_check['email'].lower() == user_new['email'].lower():
            users_duplicate_count = users_duplicate_count + 1
            user_exists = True
            break
    if not user_exists:
        # Check for duplicates already in the Prisma Cloud Account
        for user_old in user_list_old:
            if user_new['email'].lower() == user_old['email'].lower():
                users_skipped_count = users_skipped_count + 1
                user_exists = True
                break
        if not user_exists:
            user_new_temp = {}
            user_new_temp['email'] = user_new['email']
            user_new_temp['firstName'] = user_new['firstName']
            user_new_temp['lastName'] = user_new['lastName']
            user_new_temp['timeZone'] = 'America/Los_Angeles'
            user_new_temp['roleId'] = user_role_id
            users_list_new_formatted.append(user_new_temp)
            users_added_count = users_added_count + 1
print('Done.')

print('Users to add: ' + str(users_added_count))
print('Users skipped (Duplicates): ' + str(users_skipped_count))
print('Users removed as duplicates from CSV: ' + str(users_duplicate_count))

print('API - Adding users...')
for user_new in users_list_new_formatted:
    print('Adding user email: ' + user_new['email'])
    pc_settings, response_package = pc_lib_api.api_user_add(pc_settings, user_new)
print('Done.')
