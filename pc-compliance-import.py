from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import pc_lib_api
import pc_lib_general


# --Helper Functions (Local)-- #
def search_list_value(list_to_search, field_to_search, field_to_return, search_value):
    item_to_return = None
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                item_to_return = source_item[field_to_return]
                break
    return item_to_return


def search_list_value_lower(list_to_search, field_to_search, field_to_return, search_value):
    item_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                item_to_return = source_item[field_to_return]
                break
    return item_to_return


def search_list_object(list_to_search, field_to_search, search_value):
    object_to_return = None
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                object_to_return = source_item
                break
    return object_to_return


def search_list_object_lower(list_to_search, field_to_search, search_value):
    object_to_return = None
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_to_return = source_item
                break
    return object_to_return


def search_list_list(list_to_search, field_to_search, search_value):
    object_list_to_return = []
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search] == search_value:
                object_list_to_return.append(source_item)
                break
    return object_list_to_return


def search_list_list_lower(list_to_search, field_to_search, search_value):
    object_list_to_return = []
    search_value = search_value.lower()
    for source_item in list_to_search:
        if field_to_search in source_item:
            if source_item[field_to_search].lower() == search_value:
                object_list_to_return.append(source_item)
                break
    return object_list_to_return


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

parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='(Optional) - Override user input for verification (auto answer for yes).')

parser.add_argument(
    '-policy',
    '--policy',
    action='store_true',
    help='*NOT IMPLEMENTED YET*(Optional) - If you want to try update the policies with your new compliance standard, add this switch to the command.  Any policies not able to be updated will be listed out during the process.')

parser.add_argument(
    '-label',
    '--label',
    action='store_true',
    help='*NOT IMPLEMENTED YET*(Optional) - Add a label to any policy updated with the new compliance standard.  This only works if you have also specified the -policy switch.')

parser.add_argument(
    'source_import_file_name',
    type=str,
    help='Name of the file to import the new compliance standard from.')

parser.add_argument(
    'destination_compliance_standard_name',
    type=str,
    help='Name of the new compliance standard to create.')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('Ready to excute commands aginst your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        pc_lib_general.pc_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print(' Done.')

## Compliance Copy ##
# Read in the JSON import file
export_file_data = pc_lib_general.pc_file_read_json(args.source_import_file_name)

# Do a quick validation to see if we are getting the base keys
if 'compliance_standard_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'compliance_requirement_list_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'compliance_section_list_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'policy_list_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'policy_object_original' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')
if 'export_file_version' not in export_file_data:
    pc_lib_general.pc_exit_error(404, 'Data imported from file appears corrupt or incorrect for this operation.  Please check the import file name.')

# Check the compliance standard and get the JSON information
print('API - Getting the Compliance Standards list...', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list_temp = response_package['data']
compliance_standard_original = export_file_data['compliance_standard_original']
if compliance_standard_original is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard not found.  Please check the Compliance Standard name and try again.')
compliance_standard_new_temp = search_list_object_lower(compliance_standard_list_temp, 'name', args.destination_compliance_standard_name)
if compliance_standard_new_temp is not None:
    pc_lib_general.pc_exit_error(400, 'New Compliance Standard appears to already exist.  Please check the new Compliance Standard name and try again.')
print(' Done.')

# Create the new Standard
print('API - Creating the new Compliance Standard...', end='')
compliance_standard_new_temp = {}
compliance_standard_new_temp['name'] = args.destination_compliance_standard_name
if 'description' in compliance_standard_original:
    compliance_standard_new_temp['description'] = compliance_standard_original['description']
pc_settings, response_package = pc_lib_api.api_compliance_standard_add(pc_settings, compliance_standard_new_temp)
compliance_standard_new_response = response_package['data']

# Find the new Standard object
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list_temp = response_package['data']
compliance_standard_new = search_list_object(compliance_standard_list_temp, 'name', compliance_standard_new_temp['name'])
if compliance_standard_new is None:
    pc_lib_general.pc_exit_error(500, 'New Compliance Standard was not found!  Sync error?.')
print(' Done.')

# Get the list of requirements that need to be created
print('FILE - Getting Compliance Standard Requirements...', end='')
compliance_requirement_list_original = export_file_data['compliance_requirement_list_original']
print(' Done.')

# Create the new requirements
print('API - Creating the Requirements and adding them to the new Standard...', end='')
for compliance_requirement_original_temp in compliance_requirement_list_original:
    compliance_requirement_new_temp = {}
    compliance_requirement_new_temp['name'] = compliance_requirement_original_temp['name']
    compliance_requirement_new_temp['requirementId'] = compliance_requirement_original_temp['requirementId']
    if 'description' in compliance_requirement_original_temp:
        compliance_requirement_new_temp['description'] = compliance_requirement_original_temp['description']
    pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_add(pc_settings, compliance_standard_new['id'], compliance_requirement_new_temp)
print(' Done.')

# Get new list of requirements
print('API - Getting the new list of requirements...', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_list_get(pc_settings, compliance_standard_new['id'])
compliance_requirement_list_new = response_package['data']
print(' Done.')

# Get list of sections and create for each requirement section
print('API - Get list of sections, create them, and associate them to the new requirements (might take a while)...', end='')
# Create mapping list source for policy updates later
map_section_list = []
for compliance_requirement_original_temp in compliance_requirement_list_original:

    # Get sections for requirement
    compliance_section_list_original_temp = export_file_data['compliance_section_list_original'][compliance_requirement_original_temp['id']]

    # Find new ID for requirement
    compliance_requirement_new_temp = search_list_object(compliance_requirement_list_new, 'name', compliance_requirement_original_temp['name'])

    # Create new sections under new ID
    for compliance_section_original_temp in compliance_section_list_original_temp:
        compliance_section_new_temp = {}
        compliance_section_new_temp['sectionId'] = compliance_section_original_temp['sectionId']
        if 'description' in compliance_section_original_temp:
            compliance_section_new_temp['description'] = compliance_section_original_temp['description']
            pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_add(pc_settings, compliance_requirement_new_temp['id'], compliance_section_new_temp)

        # Add entry for mapping table for Policy updates later
        compliance_section_new_temp['requirementGUIDOriginal'] = compliance_requirement_original_temp['id']
        compliance_section_new_temp['requirementGUIDNew'] = compliance_requirement_new_temp['id']
        compliance_section_new_temp['sectionGUIDOriginal'] = compliance_section_original_temp['id']
        compliance_section_new_temp['sectionGUIDNew'] = None
        map_section_list.append(compliance_section_new_temp)
print(' Done.')
