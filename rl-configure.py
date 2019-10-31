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

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
if args.username is not None and args.password is not None and args.uiurl is not None:
    rl_lib_general.rl_settings_write(args.username, args.password, args.uiurl)
    print('Settings successfully saved to disk.')
elif args.username is None and args.password is None and args.uiurl is None:
    rl_settings = rl_lib_general.rl_settings_read()
    print("Your currently configured Prisma Cloud Access Key is:")
    print(rl_settings['username'])
    if rl_settings['apiBase'] is not None:
        print("Your currently configured Prisma Cloud API Base URL is:")
        print(rl_settings['apiBase'])
else:
    rl_lib_general.rl_exit_error(400,"Please input an Access Key (--username), Secret Key (--password), and UI base URL (--uiurl)"
                                 " or no switches at all to see currently set information.  Note: The Prisma Cloud UI Base URL should be "
                                 "similar to app.prismacloud.io, app2.prismacloud.io, etc.")