""" Set the Status (enable or disable) of a Policy """

import sys

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()

parser.add_argument(
    'id',
    type=str,
    help='Set Policies Severity by Id')
parser.add_argument(
    'status',
    type=str,
    choices=['true', 'false'],
    help="Policy Status to set ('true' or 'false')")
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Helpers-- #

# --Main-- #

print('API - Updating Policy Status ...', end='')
pc_api.policy_status_update(args.id, args.status)
print(' done.')


