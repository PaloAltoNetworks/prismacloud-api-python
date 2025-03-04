""" Get a Count of Protected Containers """

# pylint: disable=import-error
from prismacloudapi import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
args = parser.parse_args()

# --Helpers-- #


# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

defenders = pc_api.defenders_list_read()
accounts = {' Unknown Unknown': 0}

for defender in defenders:
    if 'provider' in defender['cloudMetadata'] and 'accountID' in defender['cloudMetadata']:
        account = f"{defender['cloudMetadata']['provider']} {defender['cloudMetadata']['accountID']}"
        if account in accounts:
            accounts[account] += 1
        else:
            accounts[account] = 1
    else:
        accounts[' Unknown Unknown'] += 1

for account in sorted(accounts.keys()):
    print(f'Cloud Account: {account}')
    print(f'  Defenders: {accounts[account]}')
    print(f'  Credits Used: {accounts[account] * 7}')
    print()
