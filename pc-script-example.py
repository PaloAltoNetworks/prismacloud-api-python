""" Example of Prisma Cloud (and Compute) API Access """

from pc_lib import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
# INSERT ARGS HERE
args = parser.parse_args()

# --Initialize-- #

pc_utility.prompt_for_verification_to_continue(args)
settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# REPLACE CODE HERE

print()
print('Prisma Cloud API Test:')
print()
result = pc_api.current_user()
print(result)

if pc_api.api_compute:
    print()
    print('Prisma Cloud Compute API Test:')
    print()
    result = pc_api.statuses_intelligence()
    print(result)

print()
print('Prisma Cloud PrismaCloudAPI Class Status:')
print()
print(pc_api)
