from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import rl_api_lib


def api_user_role_list_get(jwt, api_base):
    action = "GET"
    url = "https://" + api_base + "/user/role"
    return rl_api_lib.rl_call_api(action, url, jwt=jwt)


def api_user_list_get(jwt, api_base):
    action = "GET"
    url = "https://" + api_base + "/user"
    return rl_api_lib.rl_call_api(action, url, jwt=jwt)


def api_user_get(jwt, api_base, useremail):
    action = "GET"
    url = "https://" + api_base + "/user/" + useremail
    return rl_api_lib.rl_call_api(action, url, jwt=jwt)


def api_user_update(jwt, api_base, user_to_update):
    action = "PUT"
    url = "https://" + api_base + "/user/" + user_to_update['email']
    return rl_api_lib.rl_call_api(action, url, jwt=jwt, data=user_to_update)


# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required if no settings file has been created* - Redlock API UserName that you want to set to access your Redlock account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required if no settings file has been created* - Redlock API password that you want to set to access your Redlock account.')

parser.add_argument(
    '-c',
    '--customername',
    type=str,
    help='*Required if no settings file has been created* - Name of the Redlock account to be used.')

parser.add_argument(
    '-url',
    '--uiurl',
    type=str,
    help='*Required if no settings file has been created* - Base URL used in the UI for connecting to Redlock.  '
         'Formatted as app.redlock.io or app2.redlock.io or app.eu.redlock.io, etc.')

parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='(Optional) - Override user input for verification (auto answer for yes).')

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
rl_login_settings = rl_api_lib.rl_login_get(args.username, args.password, args.customername, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('This action will be done against the customer account name of "' + rl_login_settings['customerName'] + '".')
    verification_response = str(input('Is this correct (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        rl_api_lib.rl_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
jwt = rl_api_lib.rl_jwt_get(rl_login_settings)
apiBase = rl_login_settings['apiBase']
print('Done.')

print('API - Getting current user list...', end='')
user_list_old = api_user_list_get(jwt, apiBase)
print('Done.')

update_needed = False
user_found = False
user_new = None

print('API - Getting current user...', end='')
for user_old in user_list_old:
    if args.useremail.lower() == user_old['email'].lower():
        user_new = api_user_get(jwt, apiBase, user_old['email'])
        user_found = True
        break
if user_new is None:
    rl_api_lib.rl_exit_error(400, 'No user with that email found.  Please check the email address and try again.')
print('Done.')

# Figure out what was updated and then post the changes as a complete package
if args.role is not None:
    print('API - Getting user roles list...', end='')
    user_role_list = api_user_role_list_get(jwt, apiBase)
    print('Done.')

    print('Searching for role name to get role ID...', end='')
    for user_role in user_role_list:
        if user_role['name'].lower() == args.role.lower():
            user_new['roleId'] = user_role['id']
            update_needed = True
            break
    if update_needed is False:
        rl_api_lib.rl_exit_error(400, 'No role by that name found.  Please check the role name and try again.')
    print('Done.')
if args.firstname is not None:
    user_new['firstName'] = args.firstname
    update_needed = True
if args.lastname is not None:
    user_new['lastName'] = args.lastname
    update_needed = True

print('API - Updating user...', end='')
user_update_response = api_user_update(jwt, apiBase, user_new)
print('Done.')
