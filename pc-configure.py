from __future__ import print_function
import pc_lib_general


# --Execution Block-- #

# --Parse command line arguments-- #
parser = pc_lib_general.pc_arg_parser_defaults()

args = parser.parse_args()
# --End parse command line arguments-- #


# --Main-- #
print("Configuration file:")
if args.config_file is None:
	print(pc_lib_general.DEFAULT_SETTINGS_FILE_NAME)
else:
	print(args.config_file)
print()

if args.username is not None and args.password is not None and args.uiurl is not None:
    pc_lib_general.pc_settings_write(args.username, args.password, args.uiurl, args.config_file)
    print('Settings saved to configuration file.')
elif args.username is None and args.password is None and args.uiurl is None:
    pc_settings = pc_lib_general.pc_settings_read(args.config_file)
    print("Your currently configured Prisma Cloud Access Key is:")
    print(pc_settings['username'])
    print()
    if pc_settings['apiBase'] is not None:
        print("Your currently configured Prisma Cloud API/UI Base URL is:")
        print(pc_settings['apiBase'])
        print()
else:
    pc_lib_general.pc_exit_error(400,"Please specify an Access Key (--username), Secret Key (--password), and API/UIUI Base URL (--uiurl) "
                                 "or no switches, other than an optional (--config_file), to view your current settings. "
                                 "Note: The Prisma Cloud API/UI Base URL should be similar to: app.prismacloud.io, app2.prismacloud.io, etc.")