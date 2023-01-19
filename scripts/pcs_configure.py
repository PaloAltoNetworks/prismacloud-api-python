""" Configure """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Initialize-- #

pc_api.configure(pc_utility.get_settings(args))

# --Main-- #

# (Sync with get_arg_parser() in pc_lib_utility.py.)

if args.save is False:
    print()

    if pc_api.name:
        print('# Prisma Cloud Tenant (or Compute Console) Name:')
        print(pc_api.name)
        print()

    if pc_api.api:
        print('# Prisma Cloud API URL:')
        print(pc_api.api)
        print()

    if pc_api.api_compute:
        print('# Prisma Cloud Compute API URL:')
        print(pc_api.api_compute)
        print()

    print('# Prisma Cloud Access Key (or Compute Username):')
    print(pc_api.identity)
    print()

    print('# Prisma Cloud Secret Key (or Compute Password):')
    print(pc_api.secret)
    print()

    print('# SSL Verification:')
    print(pc_api.verify)
    print()
