from __future__ import print_function
import pc_lib_general


# --Execution Block-- #
# --Parse command line arguments-- #
parser = pc_lib_general.pc_arg_parser_defaults()

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
print(args.uiurl)
if args.username is not None and args.password is not None and args.uiurl is not None:
    pc_lib_general.pc_settings_write(args.username, args.password, args.uiurl)
    print('Settings successfully saved to disk.')
elif args.username is None and args.password is None and args.uiurl is None:
    pc_settings = pc_lib_general.pc_settings_read()
    print("Your currently configured Prisma Cloud Access Key is:")
    print(pc_settings['username'])
    if pc_settings['apiBase'] is not None:
        print("Your currently configured Prisma Cloud API Base URL is:")
        print(pc_settings['apiBase'])
else:
    pc_lib_general.pc_exit_error(400,"Please input an Access Key (--username), Secret Key (--password), and UI base URL (--uiurl)"
                                 " or no switches at all to see currently set information.  Note: The Prisma Cloud UI Base URL should be "
                                 "similar to app.prismacloud.io, app2.prismacloud.io, etc.")