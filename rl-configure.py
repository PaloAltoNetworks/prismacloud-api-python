from __future__ import print_function
import argparse
import rl_api_lib


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

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
if args.username is not None and args.password is not None and args.customername is not None:
    rl_api_lib.rl_settings_write(args.username, args.password, args.customername)
    print('Settings successfully saved to disk.')
elif args.username is None and args.password is None and args.customername is None:
    rl_settings = rl_api_lib.rl_settings_read()
    print("Your currently configured Redlock UserName is:")
    print(rl_settings['username'])
    print("Your currently configured Redlock CustomerName is:")
    print(rl_settings['customerName'])
else:
    rl_api_lib.rl_exit_error(400,"Please input a username (-u), password (-p), and customer name (-c) or no switches at all to see currently set information.")

