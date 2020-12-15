from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import json
import pc_lib_api
import pc_lib_general


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
    'compliance_standard_name',
    type=str,
    help='Name of the compliance standard to look up.  Please enter it exactly as listed in the Prisma Cloud UI')

parser.add_argument(
    '-rid',
    '--requirementId',
    type=str,
    help='*Optional* - Only required to find the UUID of a Requirement or a Section.  This will be the "REQUIREMENT" from the UI.'
         'Note: This requirement must exist in the specified Standard.  If it is in another standard, '
         'the lookup will fail.')

parser.add_argument(
    '-sid',
    '--sectionId',
    type=str,
    help='*Optional* - Only required to find the UUID of a Section.  This will be the "SECTION" from the UI.'
         'Note: This section must exist in the specified Standard and the specified Requirement.  If it is in another standard, '
         'or another Requirement, the lookup will fail.')


args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #

# Check args to make sure everything is entered that needs to be for the tiers
if args.sectionId is not None:
    if args.requirementId is None:
        pc_lib_general.pc_exit_error(400, 'A Requirement is required if you want to get the UUID of a Section.  '
            'Please enter the correct Requrement for the desired Section.  Exiting...')

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
print('Done.')

## Begin lookup ##
# Get the compliance standard list
print('API - Getting the Compliance Standards list...', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list = response_package['data']

# Search the complaince standard list for the correct Standard
compliance_standard = pc_lib_general.search_list_object_lower(compliance_standard_list, 'name', args.compliance_standard_name)
if compliance_standard is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard not found.  Please check the Compliance Standard name and try again.')
print('Done.')

# Print out the UUID for the compliance standard
print()
print('Compliance standard UUID for ' + compliance_standard['name'] + ":")
print(compliance_standard['id'])
print()

# Check to see if there is a requirement to look up as well
if args.requirementId is not None:

    # Get the list of requirements
    print('API - Getting Compliance Standard Requirements...', end='')
    pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_list_get(pc_settings, compliance_standard['id'])
    compliance_requirement_list = response_package['data']

    # Search the complaince standard requirement list for the correct requirement
    compliance_requirement = pc_lib_general.search_list_object_lower(compliance_requirement_list, 'requirementId', args.requirementId)
    if compliance_requirement is None:
        pc_lib_general.pc_exit_error(400, 'Compliance Requirement not found in the specified standard.  '
        'Please check the Compliance Standard and Requirement name and try again.')
    print('Done.')

    # Print out the UUID for the compliance standard requirement
    print()
    print('Compliance Requirement UUID for ' + compliance_requirement['requirementId'] + ":")
    print(compliance_requirement['id'])
    print()

    # Check to see if there is a section to look up as well
    if args.sectionId is not None:

        # Get the list of sections
        print('API - Getting Compliance Standard Requirements Sections...', end='')
        pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement['id'])
        compliance_section_list = response_package['data']
        print('Done.')

        # Search the complaince standard requirement section list for the correct section
        compliance_section = pc_lib_general.search_list_object_lower(compliance_section_list, 'sectionId', args.sectionId)
        if compliance_section is None:
            pc_lib_general.pc_exit_error(400, 'Compliance Section not found in the specified Requirement.  '
            'Please check the Compliance Standard, Requirement, and Section name and try again.')

        # Print out the UUID for the compliance standard requirement section
        print()
        print('Compliance Section UUID for ' + compliance_section['sectionId'] + ":")
        print(compliance_section['id'])
        print()
