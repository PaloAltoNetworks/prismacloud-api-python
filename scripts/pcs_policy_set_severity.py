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
    'severity',
    type=str,
    choices=['low', 'high', 'informational', 'medium', 'critical'],
    help="Policy Severity to set ('low', 'high', 'informational', 'medium' or 'critical')")
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Helpers-- #

# --Main-- #

print('API - Retrieving Policy Information ...', end='')
policy_to_update = pc_api.policy_read(args.id)
print(' done.')

policy_to_update['severity'] = args.severity

print('API - Updating Policy Severity ...', end='')
pc_api.policy_update(args.id,policy_to_update)
print(' done.')


