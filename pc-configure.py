from __future__ import print_function
import pc_lib_general

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
args = parser.parse_args()

# --Main-- #

print('Configuration File:')
if args.config_file is None:
	print(pc_lib_general.DEFAULT_SETTINGS_FILE_NAME)
else:
	print(args.config_file)
print()

if args.username is not None and args.password is not None and args.uiurl is not None:
    pc_lib_general.pc_settings_file_write(args)
    print('Settings saved.')
elif args.username is None and args.password is None and args.uiurl is None:
    pc_settings = pc_lib_general.pc_settings_file_read(args.config_file)
    if pc_settings['apiBase'] is not None:
        print('Prisma Cloud API/UI Base URL:')
        print(pc_settings['apiBase'])
        print()
    if pc_settings['username'] is not None:
        print('Prisma Cloud Access Key:')
        print(pc_settings['username'])
        print()
    if pc_settings['password'] is not None:
        print('Prisma Cloud Secret Key:')
        print(pc_settings['password'])
        print()
    if pc_settings['ca_bundle'] is not None:
        print('(Optional) Custom CA (bundle) file:')
        print(pc_settings['ca_bundle'])
        print()
    print('-u %s -p %s --uiurl %s --ca_bundle %s' % (pc_settings['username'], pc_settings['password'], pc_settings['ca_bundle'], pc_settings['ca_bundle']))
else:
    print('Please specify an Access Key (-u / --username), Secret Key (-p / --password), and API/UI Base URL (-url / --uiurl) to save your configuration.')
    print()
    print('Please specify nothing, other than an optional (--config_file), to view your current configuration.')
