from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import rl_lib_api
import rl_lib_general


# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required* - Prisma Cloud API Access Key ID that you want to set to access your Prisma Cloud account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required* - Prisma Cloud API Secret Key that you want to set to access your Prisma Cloud account.')

parser.add_argument(
    '-url',
    '--uiurl',
    type=str,
    help='*Required* - Base URL used in the UI for connecting to Prisma Cloud.  '
         'Formatted as app.prismacloud.io or app2.prismacloud.io or app.eu.prismacloud.io, etc.  '
         'You can also input the api version of the URL if you know it and it will be passed through.')
parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='(Optional) - Override user input for verification (auto answer for yes).')

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
rl_settings = rl_lib_general.rl_login_get(args.username, args.password, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to excute commands aginst your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        rl_lib_general.rl_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
rl_settings = rl_lib_api.rl_jwt_get(rl_settings)
print('Done.')

print('API - Getting current user list...', end='')
rl_settings, response_package = rl_lib_api.api_user_list_get(rl_settings)
user_list_old = response_package['data']
print('Done.')

print('File - Loading CSV user data...', end='')
user_list_new = rl_lib_general.rl_file_load_csv(args.importfile)
print('Done.')

print('API - Getting user roles...', end='')
rl_settings, response_package = rl_lib_api.api_user_role_list_get(rl_settings)
user_role_list = response_package['data']
print('Done.')

print('Searching for role name to get role ID...', end='')
user_role_id = None
for user_role in user_role_list:
    if user_role['name'].lower() == args.userrolename.lower():
        user_role_id = user_role['id']
        break
if user_role_id is None:
    rl_lib_general.rl_exit_error(400, 'No role by that name found.  Please check the role name and try again.')
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
        # Check for duplicates already in the Redlock Account
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
    rl_settings, response_package = rl_lib_api.api_user_add(rl_settings, user_new)
print('Done.')
