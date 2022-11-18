""" Export a specific Compliance Standard """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION = 3

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--concurrency',
    type=int,
    default=0,
    help='(Optional) - Number of concurrent API calls. (1-16)')
parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard to export.')
parser.add_argument(
    'export_file_name',
    type=str,
    help='Export file name for the Compliance Standard.')
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

# Compliance Export

export_file_data = {}
export_file_data['export_file_version'] = DEFAULT_COMPLIANCE_EXPORT_FILE_VERSION
export_file_data['compliance_section_list_original'] = {}
export_file_data['policy_list_original'] = []
export_file_data['policy_object_original'] = {}
export_file_data['search_object_original'] = {}

print('API - Getting the current list of Compliance Standards ...', end='')
compliance_standard_list_current = pc_api.compliance_standard_list_read()
compliance_standard_original = pc_utility.search_list_object_lower(compliance_standard_list_current, 'name', args.compliance_standard_name)
if compliance_standard_original is None:
    pc_utility.error_and_exit(400, 'Compliance Standard to export not found. Please verify the Compliance Standard name.')
export_file_data['compliance_standard_original'] = compliance_standard_original
print(' done.')
print()

print('API - Getting the Compliance Standard Requirements ...', end='')
compliance_requirement_list_original = pc_api.compliance_standard_requirement_list_read(compliance_standard_original['id'])
export_file_data['compliance_requirement_list_original'] = compliance_requirement_list_original
print(' done.')
print()

print('API - Getting the Compliance Standard Sections ...', end='')
for compliance_requirement_original in compliance_requirement_list_original:
    compliance_section_list_original = pc_api.compliance_standard_requirement_section_list_read(compliance_requirement_original['id'])
    export_file_data['compliance_section_list_original'][compliance_requirement_original['id']] = compliance_section_list_original
print(' done.')
print()

print('API - Getting the Compliance Standard Policy List (please wait) ...', end='')
policy_list_current = pc_api.compliance_standard_policy_v2_list_read(compliance_standard_original['name'])
export_file_data['policy_list_original'] = policy_list_current
print(' done.')
print()

# Threaded Queries.
result = pc_api.get_policies_with_saved_searches(policy_list_current)

export_file_data['policy_object_original'] = result['policies']
export_file_data['search_object_original'] = result['searches']
pc_utility.write_json_file(args.export_file_name, export_file_data)
print('Exported to: %s' % args.export_file_name)
