""" Export Custom Policies """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

DEFAULT_POLICY_EXPORT_FILE_VERSION = 2

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--concurrency',
    type=int,
    default=0,
    help='(Optional) - Number of concurrent API calls. (1-16)')
parser.add_argument(
    'export_file_name',
    type=str,
    help='Export file name for the Custom Policies.')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Avoid API rate limits.
if args.concurrency > 0 and args.concurrency <= 16:
    pc_api.max_workers = args.concurrency
print('Limiting concurrent API calls to: (%s)' % pc_api.max_workers)
print()

# Policy Custom Export

export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_POLICY_EXPORT_FILE_VERSION
export_file_data['policy_list_original'] = []
export_file_data['policy_object_original'] = {}
export_file_data['search_object_original'] = {}

print('API - Getting the current list of Custom Policies ...', end='')
policy_list_current = pc_api.policy_custom_v2_list_read()
export_file_data['policy_list_original'] = policy_list_current
print(' done.')
print()

# Threaded Queries.
result = pc_api.get_policies_with_saved_searches(policy_list_current)

export_file_data['policy_object_original'] = result['policies']
export_file_data['search_object_original'] = result['searches']
pc_utility.write_json_file(args.export_file_name, export_file_data)
print('Exported to: %s' % args.export_file_name)
