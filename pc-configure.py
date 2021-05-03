from __future__ import print_function
import pc_lib_general

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Main-- #

print('Configuration File:')
if args.config_file is None:
	print(pc_utility.DEFAULT_SETTINGS_FILE_NAME)
else:
	print(args.config_file)
print()

if args.username is not None and args.password is not None and args.uiurl is not None:
    pc_utility.write_settings_file(args)
    print('Settings saved.')
elif args.username is None and args.password is None and args.uiurl is None:
    settings = pc_utility.read_settings_file(args.config_file)
    if settings['apiBase'] is not None:
        print('Prisma Cloud API/UI Base URL:')
        print(settings['apiBase'])
        print()
    if settings['username'] is not None:
        print('Prisma Cloud Access Key:')
        print(settings['username'])
        print()
    if settings['password'] is not None:
        print('Prisma Cloud Secret Key:')
        print(settings['password'])
        print()
    if settings['ca_bundle'] is not None:
        print('(Optional) Custom CA (bundle) file:')
        print(settings['ca_bundle'])
        print()
    print('-u %s -p %s --uiurl %s --ca_bundle %s' % (settings['username'], settings['password'], settings['ca_bundle'], settings['ca_bundle']))
else:
    print('Please specify an Access Key (-u / --username), Secret Key (-p / --password), and API/UI Base URL (-url / --uiurl) to save your configuration.')
    print()
    print('Please specify nothing, other than an optional (--config_file), to view your current configuration.')
