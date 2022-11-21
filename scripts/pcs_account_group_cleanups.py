""" Import Account Groups from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import (CSV) file name for the Account Groups.')
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

print('API - Getting the current list of Account Groups ...', end='')
cloud_account_group_list_current = pc_api.cloud_account_group_list_read()
print(' done.')
print()

cloud_account_group_list_to_import = pc_utility.read_csv_file_text(args.import_file_name)

cloud_account_groups_duplicate_current_count = 0

cloud_account_groups_to_import = []
for cloud_account_group_to_import in cloud_account_group_list_to_import:
    cloud_account_group_duplicate = False
    #if len(cloud_account_group_list_to_import) > 1:
        # Remove duplicates from the import file list.
    #    for cloud_account_group_to_import_inner in cloud_account_group_list_to_import:
    #        if cloud_account_group_to_import['email'].lower() == cloud_account_group_to_import_inner['email'].lower():
    #            cloud_account_groups_duplicate_file_count = cloud_account_groups_duplicate_file_count + 1
    #            cloud_account_group_duplicate = True
    #            break
    if not cloud_account_group_duplicate:
        # Remove duplicates based upon the current cloud_account_group list.
        for cloud_account_group_current in cloud_account_group_list_current:
            if cloud_account_group_to_import['name'].lower() == cloud_account_group_current['name'].lower():
                cloud_account_groups_duplicate_current_count = cloud_account_groups_duplicate_current_count + 1
                cloud_account_group_duplicate = True
                break
    if not cloud_account_group_duplicate:
        cloud_account_group = {}
        cloud_account_group['name'] = cloud_account_group_to_import['name']
        cloud_account_group['description'] = cloud_account_group_to_import['description']
        cloud_account_group['accountIds'] = []
        cloud_account_groups_to_import.append(cloud_account_group)

print('Cloud Account Groups to add: %s' % len(cloud_account_groups_to_import))
print('Cloud Account Groups skipped (duplicates in Prisma Cloud): %s' % cloud_account_groups_duplicate_current_count)

print('API - Creating Cloud Account Groups ...')
for cloud_account_group_to_import in cloud_account_groups_to_import:
    print('Adding Cloud Account Group: %s' % cloud_account_group_to_import['name'])
    pc_api.cloud_account_group_update(cloud_account_group_to_import)
print('Done.')
