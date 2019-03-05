from __future__ import print_function
import argparse
import rl_lib_general


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
    '-url',
    '--uiurl',
    type=str,
    help='*Required* - Base URL used in the UI for connecting to Redlock.  '
         'Formatted as app.redlock.io or app2.redlock.io or app.eu.redlock.io, etc.')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
if args.username is not None and args.password is not None and args.customername is not None and args.uiurl is not None:
    rl_lib_general.rl_settings_write(args.username, args.password, args.customername, args.uiurl)
    print('Settings successfully saved to disk.')
elif args.username is None and args.password is None and args.customername is None:
    rl_settings = rl_lib_general.rl_settings_read()
    print("Your currently configured Redlock UserName is:")
    print(rl_settings['username'])
    print("Your currently configured Redlock CustomerName is:")
    print(rl_settings['customerName'])
    if rl_settings['apiBase'] is not None:
        print("Your currently configured Redlock API Base URL is:")
        print(rl_settings['apiBase'])
else:
    rl_lib_general.rl_exit_error(400,"Please input a username (-u), password (-p), customer name (-c), and UI base URL (-url)"
                                 " or no switches at all to see currently set information.  Note: The Redlock UI Base URL should be "
                                 "similar to app.redlock.io, app2.redlock.io, etc.")
