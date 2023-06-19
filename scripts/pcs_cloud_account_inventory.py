# pylint: disable=redefined-outer-name
""" Add discovered registries to Vulnerability->Images->Registry settings """

import csv

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
        '--output',
        default='output.csv',
        type=str,
        help='(Optional) - Name of output file, defaults to output.csv')
args = parser.parse_args()

# --Helpers-- #

def process_account(acct_obj,parent):
    if acct_obj['numberOfChildAccounts'] > 0:
        c_accounts=pc_api.cloud_accounts_children_list_read(acct_obj['cloudType'],acct_obj['accountId'])
        for account in c_accounts:
            process_account(account,acct_obj['accountId'])
    if acct_obj['numberOfChildAccounts'] > 0 and parent == "":
        pass
    else:
        a_dict = {
            "name"      : acct_obj['name'],
            "cloud"     : acct_obj['cloudType'],
            "parent"    : parent,
            "type"      : acct_obj['accountType'],
            "id"        : acct_obj['accountId']
        }
        master_account_list.append(a_dict)
    return 0

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Initialize-- #

cloud_accounts_list = pc_api.cloud_accounts_list_read()
master_account_list=[]
for account in cloud_accounts_list:
    process_account(account,"")

keys = master_account_list[0].keys()
with open(args.output, 'w', newline='') as a_file:
    dict_writer = csv.DictWriter(a_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(master_account_list)
