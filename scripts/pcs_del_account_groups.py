""" Import Account Groups from a CSV file """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility
import numpy as np
import json

parser = pc_utility.get_arg_parser()
parser.add_argument(
    'prefix',
    type=str,
    help='The prefix of account groups')
args = parser.parse_args()

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
prefix_length=len(args.prefix)

# --Main-- #

print('API - Getting the current list of account groups ...', end='')
cloud_account_group_list_current = pc_api.cloud_account_group_list_read()
print(' done.')
print()

## --Delete User-- #

account_group_to_delete = []

for cloud_acount_group_current in cloud_account_group_list_current:
    if cloud_acount_group_current['name'][0:prefix_length] == args.prefix:
        print('Deleting account group found with name: %s' % cloud_acount_group_current['name'].lower())
        cloud_account_group = cloud_acount_group_current
        cloud_account_group['accountIds'] = []
        pc_api.cloud_account_group_update(cloud_acount_group_current['id'],cloud_account_group)
        pc_api.cloud_account_group_delete(cloud_acount_group_current['id'])

print('done.')
print()


