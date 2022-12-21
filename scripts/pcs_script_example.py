""" Example of Prisma Cloud (and Compute) API Access """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
# ADD SCRIPT-SPECIFIC ARGS HERE
parser.add_argument('--example', type=str, default='', help='(Optional) - Example')
args = parser.parse_args()

# --Initialize-- #

pc_api.configure(pc_utility.get_settings(args))

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

if pc_api.api_compute:
    print()
    print('Prisma Cloud Compute API Test:')
    print()
    print(pc_api.statuses_intelligence())
    print()

if pc_api.api:
    print()
    print('Prisma Cloud Code Security API Test:')
    print()
    print('Checkov Version: %s' % pc_api.checkov_version())
    print()

print(pc_api)
print()
