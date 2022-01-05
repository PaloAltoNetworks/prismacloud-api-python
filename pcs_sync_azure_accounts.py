""" Synchronize Azure Accounts from PC to PCC """

from __future__ import print_function
import json
import sys
from operator import itemgetter
from pc_lib import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--tenant',
    type=str,
    required=True,
    help='Account ID of Tenant to sync.')
parser.add_argument(
    '--dryrun',
    action='store_true',
    help='Set flag for dryrun mode')
parser.add_argument(
    '--service_key',
    default=None,
    type=str,
    help='(Optional) - Path to file containing Tenant\'s AZ SP Service Key')
args = parser.parse_args()


# --Helpers-- #
def read_service_key(service_key_file):
    try:
        json_key = open(service_key_file, 'rb')
        print(' Success.')
    except OSError:
        print(' Error.')
        print ('ERROR - Could not open/read file: %s' % service_key_file)
        sys.exit()
    with json_key:
        service_key = json.load(json_key)
    return service_key

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

print('INFO  - Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' Success.')

print('API   - Getting the current list of Cloud Accounts ...', end='')
cloud_accounts_list = pc_api.cloud_accounts_list_read()
print(' Success.')

print('API   - Getting the current list of Compute Credentials ...', end='')
compute_credential_list = pc_api.credential_list_read()
print(' Success.')

# If args.service_key is defined, open file and compare tenant id
# to args.tenant.
# If successful, store service key as dictionary: service_key
if args.service_key:
    print('INFO  - Opening Service Key File ...', end='')
    service_key_dict = read_service_key(args.service_key)
    print('INFO  - Validate Service Key ...', end='')
    if service_key_dict['tenantId'] != args.tenant:
        print(' Error.')
        print('ERROR - Service Key provided does not match requested '
              'tenant: %s' % args.tenant)
        sys.exit()
    print(' Success.')

# Build list of cloud accounts with account id's that match input args.tenant
# There should be only one match.  If not, the account wasn't on-boarded or
# there is an error with the data.
tenant_name = list(map(itemgetter('name'), (
    list(
        filter(
            lambda item: (
                (item['accountId'] == args.tenant) and
                (item['accountType'] == 'tenant')
            ), cloud_accounts_list
        )
    ))))
print('INFO  - Validate tenant credential to be added to compute ...', end='')
if len(tenant_name) < 1:
    print(' Error.')
    print('ERROR - Could not find tenant \"%s\" in Prisma Cloud Accounts.'
          % args.tenant)
    sys.exit()
elif len(tenant_name) > 1:
    print(' Error.')
    print('ERROR - Too many Prisma Cloud Accounts matched tenant \"%s\".'
          % args.tenant)
else:
    tenant_name = ' '.join(map(str, tenant_name))
    print(' Success.')

print('API   - Getting all children accounts in tenant ...', end='')
children = pc_api.cloud_accounts_children_list_read('azure', args.tenant)
print(' Success.')

# var cloud_account_names = list of all tenant's children's names
# var children = list of dict for all children cloud accounts
cloud_account_names = []
for child_account in children:
    if child_account['accountType'] == 'account':
        cloud_account_names.append(child_account['name'])

if len(cloud_account_names) < 1:
    print('INFO  - No children accounts in tenant to add to compute.')

# Generate a list of Compute Credentials associated with tenant and store
# as tenant_creds.
# var tenant_name = string of name of tenant
# var tenant_creds = list of all compute credentials belonging to args.tenant
tenant_creds = []
for cred in compute_credential_list:
    if (
        ('description' in cred) and
        (tenant_name in cred['_id']) and
        (cred['type'] == 'azure')
    ):
        tenant_creds.append(cred['_id'])

# Interate through compute credential names and compare to cloud account
# tenant children.
# If not in children, remove credential from compute.
for cred in tenant_creds:
    if cred not in cloud_account_names:
        if not args.dryrun:
            print('API   - Removing credential \"%s\" from compute ...'
                  % cred, end='')
            pc_api.credential_list_delete(cred)
            print(' Success')
        else:
            print('DRYRN - Removing credential \"%s\" from compute' % cred)

# Iterate through the list of children accounts...
for child in pc_api.cloud_accounts_children_list_read('azure', args.tenant):
    # and match and child that is both accountType == "account" and is not
    # already in compute_credential_list
    if (
        (child['accountType'] == 'account') and
        (not any(d['_id'] == child['name'] for d in compute_credential_list))
    ):
        # for each child account being add, insert associated subscription
        # id into service_key
        service_key_dict['subscriptionId'] = child['accountId']
        secret = {
            'encrypted': '',
            'plain': json.dumps(service_key_dict)
        }
        # Add credential
        if not args.dryrun:
            print('API   - Adding account \"%s\" to compute credentials ...'
                  % child['name'], end='')
            pc_api.credential_list_create(
                child['name'],
                'azure',
                secret,
                'Added by automation'
            )
            print(' Success')
        else:
            print('DRYRN - Adding account \"%s\" to compute credentials'
                  % child['name'])
