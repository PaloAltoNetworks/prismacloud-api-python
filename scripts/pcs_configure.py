""" Read or write command-line parameters to a configuration file  """

from pc_lib import pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Main-- #

print('Configuration File Name:')
if args.config_file is None:
    print(pc_utility.DEFAULT_SETTINGS_FILE_NAME)
else:
    print(args.config_file)
print()

if args.username is None and args.password is None:
    settings = pc_utility.read_settings_file(args.config_file)
    pc_utility.print_settings_file(settings)
elif args.api != '' or args.api_compute != '':
    pc_utility.write_settings_file(args)
    print('Settings saved.')
else:
    print('Please specify an Access Key / Username (-u / --username), Secret Key / Password (-p / --password), and API/UI Base URL (--api or --api_compute) to save your configuration.')
    print()
    print('Please specify nothing, other than an optional (--config_file), to view your current configuration.')
print()
