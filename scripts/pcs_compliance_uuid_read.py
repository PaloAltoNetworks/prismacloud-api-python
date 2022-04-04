""" Get the UUID of a specific Compliance Standard (or Requirement or Section) """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='(Required) - Name of the Compliance Standard.')
parser.add_argument(
    '-rid',
    '--requirementId',
    type=str,
    help='(Optional) - Only required to find the UUID of a Requirement or a Section. This will be the "REQUIREMENT" from the UI. '
         'Note: This requirement must exist in the specified Compliance Standard. If it is in another standard, the lookup will fail.')
parser.add_argument(
    '-sid',
    '--sectionId',
    type=str,
    help='(Optional) - Only required to find the UUID of a Section. This will be the "SECTION" from the UI. '
         'Note: This section must exist in the specified Standard and the specified Compliance Requirement. '
         'If it is in another standard, or another Requirement, the lookup will fail.')
args = parser.parse_args()

if args.sectionId is not None:
    if args.requirementId is None:
        pc_utility.error_and_exit(400, 'A Requirement is required if you want to get the UUID of a Section. '
            'Please enter the correct Requirement for the desired Section.')

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Compliance Get UUID

print('API - Getting the Compliance Standards list ...', end='')
compliance_standard_list = pc_api.compliance_standard_list_read()
compliance_standard = pc_utility.search_list_object_lower(compliance_standard_list, 'name', args.compliance_standard_name)
print(' done.')
print()

if compliance_standard is None:
    pc_utility.error_and_exit(400, 'Compliance Standard not found. Please verify the Compliance Standard name.')

print()
print('Compliance Standard Name: ' + compliance_standard['name'] + "\nUUID: " + compliance_standard['id'])
print()

if args.requirementId is not None:
    print('API - Getting Requirements List for Compliance Standard ...', end='')
    compliance_requirement_list = pc_api.compliance_standard_requirement_list_read(compliance_standard['id'])
    print(' done.')
    print()

    compliance_requirement = pc_utility.search_list_object_lower(compliance_requirement_list, 'requirementId', args.requirementId)
    if compliance_requirement is None:
        pc_utility.error_and_exit(400, 'Requirement not found in the specified Compliance Standard. '
        'Please verify the Compliance Standard and Requirement names.')

    print()
    print('Requirement Name: ' + compliance_requirement['requirementId'] + "\nUUID: " + compliance_requirement['id'])
    print()

    if args.sectionId is not None:
        print('API - Getting Sections for Requirement ...', end='')
        compliance_section_list = pc_api.compliance_standard_requirement_section_list_read(compliance_requirement['id'])
        print(' done.')
        print()

        compliance_section = pc_utility.search_list_object_lower(compliance_section_list, 'sectionId', args.sectionId)
        if compliance_section is None:
            pc_utility.error_and_exit(400, 'Section not found in the specified Requirement.  '
            'Please verify the Compliance Standard, Requirement, and Section names.')

        print()
        print('Section Name: ' + compliance_section['sectionId'] + "\nUUID: " + compliance_section['id'])
        print()
