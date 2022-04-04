""" Example of Prisma Cloud (and Compute) API Access """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# REPLACE CODE HERE

if pc_api.api:
    print()
    print('Prisma Cloud API Test:')
    print()
    print(pc_api.current_user())
    print()
    print('Prisma Cloud Compute API Info:')
    print()
    print(pc_api.compute_config())
    print()

if pc_api.api_compute:
    print()
    print('Prisma Cloud Compute API Test:')
    print()
    print(pc_api.statuses_intelligence())
    print()
