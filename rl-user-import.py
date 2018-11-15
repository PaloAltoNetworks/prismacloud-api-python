from __future__ import print_function
import argparse
import rl_api_lib
import json


def api_user_role_list_get(jwt):
    action = "GET"
    url = "https://api.redlock.io/user/role"
    return rl_api_lib.rl_call_api(action, url, jwt=jwt)


def api_user_list_get(jwt):
    action = "GET"
    url = "https://api.redlock.io/user"
    return rl_api_lib.rl_call_api(action, url, jwt=jwt)


def api_user_add(jwt, user_to_add):
    action = "POST"
    url = "https://api.redlock.io/user"
    return rl_api_lib.rl_call_api(action, url, jwt=jwt, data=user_to_add)


# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required* - Redlock API UserName that you want to set to access your Redlock account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required* - Redlock API password that you want to set to access your Redlock account.')

parser.add_argument(
    '-c',
    '--customername',
    type=str,
    help='*Required* - Name of the Redlock account to be used.')

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
# Sort out API Login
print('API - Getting authentication token...', end='')
jwt = rl_api_lib.rl_jwt_get(args.username, args.password, args.customername)
print('Done.')

print('API - Getting current user list...', end='')
user_list_old = api_user_list_get(jwt)
print('Done.')

print('File - Loading CSV user data...', end='')
user_list_new = rl_api_lib.rl_file_load_csv(args.importfile)
print('Done.')

print('API - Getting user roles...', end='')
user_role_list = api_user_role_list_get(jwt)
print('Done.')

print('Searching for role name to get role ID...', end='')
user_role_id = None
for user_role in user_role_list:
    if user_role['name'].lower() == args.userrolename.lower():
        user_role_id = user_role['id']
        break
if user_role_id is None:
    rl_api_lib.rl_exit_error(400, 'No role by that name found.  Please check the role name and try again.')
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
    user_new_response = api_user_add(jwt, user_new)
print('Done.')
