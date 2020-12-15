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
    help='*Required* - Base URL used in the UI for connecting to Prisma Cloud. '
         'Formatted as app.prismacloud.io or app2.prismacloud.io or app.eu.prismacloud.io, etc. '
         'You can also input the api version of the URL if you know it and it will be passed through. ')

parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='*Optional* - Override user input for verification (auto answer for yes).')

parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard to look up. Please enter it exactly as listed in the Prisma Cloud UI')

parser.add_argument(
    '-rid',
    '--requirementId',
    type=str,
    help='*Optional* - Only required to find the UUID of a Requirement or a Section. This will be the "REQUIREMENT" from the UI. '
         'Note: This requirement must exist in the specified Standard. If it is in another standard, the lookup will fail.')

parser.add_argument(
    '-sid',
    '--sectionId',
    type=str,
    help='*Optional* - Only required to find the UUID of a Section. This will be the "SECTION" from the UI. '
         'Note: This section must exist in the specified Standard and the specified Requirement. '
         'If it is in another standard, or another Requirement, the lookup will fail.')

args = parser.parse_args()

# --End parse command line arguments-- #


# --Main-- #

if args.sectionId is not None:
    if args.requirementId is None:
        pc_lib_general.pc_exit_error(400, 'A Requirement is required if you want to get the UUID of a Section. '
            'Please enter the correct Requirement for the desired Section. Exiting ...')

pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl)

# Verification (override with -y)

if not args.yes:
    print()
    print('Ready to excute commands aginst your Prisma Cloud tenant.')
    verification_response = str(input('Would you like to continue (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        pc_lib_general.pc_exit_error(400, 'Verification failed due to user response. Exiting...')

# API Login

print('API - Getting authentication token... ', end='')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print('done.')

# API Queries

print('API - Getting the Compliance Standards list ... ', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list = response_package['data']
compliance_standard = search_list_object_lower(compliance_standard_list, 'name', args.compliance_standard_name)
print('done.')

if compliance_standard is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard not found. Please check the Compliance Standard name and try again.')

print()
print('Compliance Standard Name: ' + compliance_standard['name'] + "\nUUID: " + compliance_standard['id'])
print()

if args.requirementId is not None:
    print('API - Getting Requirements List for Compliance Standard ... ', end='')
    pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_list_get(pc_settings, compliance_standard['id'])
    compliance_requirement_list = response_package['data']
    print('done.')

    compliance_requirement = search_list_object_lower(compliance_requirement_list, 'requirementId', args.requirementId)
    if compliance_requirement is None:
        pc_lib_general.pc_exit_error(400, 'Requirement not found in the specified Compliance Standard. '
        'Please check the Compliance Standard and Requirement names and try again.')

    print()
    print('Requirement Name: ' + compliance_requirement['requirementId'] + "\nUUID: " + compliance_requirement['id'])
    print()

    if args.sectionId is not None:
        print('API - Getting Sections for Requirement ... ', end='')
        pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement['id'])
        compliance_section_list = response_package['data']
        print('done.')

        compliance_section = search_list_object_lower(compliance_section_list, 'sectionId', args.sectionId)
        if compliance_section is None:
            pc_lib_general.pc_exit_error(400, 'Section not found in the specified Requirement.  '
            'Please check the Compliance Standard, Requirement, and Section names and try again.')

        print()
        print('Section Name: ' + compliance_section['sectionId'] + "\nUUID: " + compliance_section['id'])
        print()