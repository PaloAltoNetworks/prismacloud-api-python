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
rl_settings = rl_lib_general.rl_login_get(args.username, args.password, args.customername, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('This action will be done against the customer account name of "' + rl_settings['customerName'] + '".')
    verification_response = str(input('Is this correct (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        rl_lib_general.rl_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
rl_settings = rl_lib_api.rl_jwt_get(rl_settings)
print('Done.')

print('API - Getting user...', end='')
rl_settings, response_package = rl_lib_api.api_user_get(rl_settings, args.useremail.lower())
user_new = response_package['data']
print('Done.')

# Figure out what was updated and then post the changes as a complete package
if args.role is not None:
    print('API - Getting user roles list...', end='')
    rl_settings, response_package = rl_lib_api.api_user_role_list_get(rl_settings)
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
        rl_lib_general.rl_exit_error(400, 'No role by that name found.  Please check the role name and try again.')
    print('Done.')
if args.firstname is not None:
    user_new['firstName'] = args.firstname
if args.lastname is not None:
    user_new['lastName'] = args.lastname

print('API - Updating user...', end='')
rl_settings, response_package = rl_lib_api.api_user_update(rl_settings, user_new)
print('Done.')
