""" Synchronize Azure Accounts from PC to PCC """

import json

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--tenantId',
    type=str,
    required=True,
    help='Account ID of Tenant to sync.')
parser.add_argument(
    '--clientId',
    type=str,
    required=True,
    help='Client Id of SPN Service Key.')
parser.add_argument(
    '--clientSecret',
    type=str,
    required=True,
    help='Client Secret of SPN Service Key.')
parser.add_argument(
    '--dryrun',
    action='store_true',
    help='Set flag for dryrun mode')
args = parser.parse_args()


# --Helpers-- #
def build_service_key(client_id, client_secret, subscription_id, tenant_id):
    return {
        "clientId": client_id,
        "clientSecret": client_secret,
        "subscriptionId": subscription_id,
        "tenantId": tenant_id,
        "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
        "resourceManagerEndpointUrl": "https://management.azure.com/",
        "activeDirectoryGraphResourceId": "https://graph.windows.net/",
        "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
        "galleryEndpointUrl": "https://gallery.azure.com/",
        "managementEndpointUrl": "https://management.core.windows.net/"
    }

# Recieves a list of dicts, with each disc representing a tenant child
# The child can be an account or mgt group so we seperate and return
# a list of only child account names
def get_children_accounts(children_ld):
    child_account_names = []
    for child_account in children_ld:
        if child_account['accountType'] == 'account':
            child_account_names.append(child_account)
            #child_account_names.append(child_account['name'])
    return child_account_names

# Receive a list of all current compute credentials and prisma cloud
# account name. Create list of all credentials that include cloud
# account name and also are of type azure and also have a description.
# Return a list of matched "children" credentials as a list of
# dictionaries.
def get_tenant_children_creds(cred_list, cloud_account_name):
    tenant_creds = []
    for c_item in cred_list:
        if (
            ('description' in c_item) and
            (cloud_account_name in c_item['_id']) and
            (c_item['type'] == 'azure')
        ):
            tenant_creds.append(c_item)
    return tenant_creds

# Receive children_creds, a list of dicts including all compute credentials
# that are attached to the cloud tenant being synchronized.
# Receive children_accounts, a list of dicts including all cloud
# children subscriptions that belong to the cloud tenant being
# synchronized.
def del_orphaned_credentials(children_creds, children_accounts):
    counter=0
    for compute_credential in children_creds:
        if [account for account in children_accounts if account['name'] == compute_credential['_id']]:
            pass
        else:
            print('INFO  - Removing credential \"%s\" from compute.'
                  % compute_credential['_id'])
            print('API   - Gathering any usage dependancies for \"%s\" ...' % compute_credential['_id'], end='')
            usage_deps = pc_api.credential_list_usages_read(compute_credential['_id'])
            print(' Success')
            if not args.dryrun:
                if usage_deps:
                    print('Info  - %s Usage Dependancies for \"%s\".' % (len(usage_deps), compute_credential['_id']))
                    for dependancy in usage_deps:
                        print('INFO  - %s configured for %s.' % (dependancy['type'], compute_credential['_id']))
                        remove_dep(dependancy['type'], compute_credential['_id'])
                else:
                    print('INFO  - No Usage Dependancies for \"%s\".' % compute_credential['_id'])
                print('API   - Removing credential \"%s\" from compute ...'
                      % compute_credential['_id'], end='')
                pc_api.credential_list_delete(compute_credential['_id'])
                print(' Success')
            else:
                print('DRYRN - Removing credential \"%s\" from compute.'
                      % compute_credential['_id'])
            counter+=1
    return counter

def remove_dep(dep_type, cred_id):
    if dep_type == 'Cloud Scan':
        print('API   - Removing %s for %s ...' % (dep_type, cred_id), end='')
        scans=pc_api.policies_cloud_platforms_read()
        scans['rules']=list(filter(lambda i: i['credentialId'] != cred_id, scans['rules']))
        pc_api.policies_cloud_platforms_write({'rules' : scans['rules']})
        print(' Success')
    if dep_type == 'Serverless Scan':
        print('API   - Removing %s for %s ...' % (dep_type, cred_id), end='')
        scans=pc_api.settings_serverless_scan_read()
        scans=list(filter(lambda i: i['credentialID'] != cred_id, scans))
        pc_api.settings_serverless_scan_write(scans)
        print(' Success')
    if dep_type == 'Registry Scan':
        print('API   - Removing %s for %s ...' % (dep_type, cred_id), end='')
        scans=pc_api.settings_registry_read()
        scans['specifications']=list(filter(lambda i: i['credentialID'] != cred_id, scans['specifications']))
        pc_api.settings_registry_write({'specifications' : scans['specifications']})
        print(' Success')
    return 0


def add_missing_credentials(children_creds, children_accounts, client_id):
    counter=0
    for cloud_account in children_accounts:
        if [account for account in children_creds if account['_id'] == cloud_account['name']]:
            pass
        else:
            print('INFO  - Adding Cloud account \"%s\" to Compute creds.'
                  % cloud_account['name'])
            secret_dict = build_service_key(
                client_id,
                args.clientSecret,
                cloud_account['accountId'],
                args.tenantId)
            secret = {
                'encrypted': '',
                'plain': json.dumps(secret_dict)
            }
            body = {
                'secret': secret,
                'serviceAccount': {},
                'type': 'azure',
                'description': 'Added by automation',
                'skipVerify': False,
                '_id': cloud_account['name']
            }
            if not args.dryrun:
                print('API   - Adding credential \"%s\" to compute ...'
                      % cloud_account['name'], end='')
                pc_api.credential_list_create(body)
                print(' Success')
            else:
                print('DRYRN - Adding credential \"%s\" to compute'
                      % cloud_account['name'])
            counter+=1
    return counter

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

print('API   - Getting the Azure Cloud Account Information ...', end='')
tenant_client_info = pc_api.cloud_account_info_read('azure', args.tenantId)
print(' Success.')

print('API   - Getting all children accounts in tenant ...', end='')
children = pc_api.cloud_accounts_children_list_read('azure', args.tenantId)
print(' Success.')

children_cloud_accounts = get_children_accounts(children)
if len(children_cloud_accounts) < 1:
    print('INFO  - No children accounts in tenant to add to compute.')
else:
    print('INFO  - Number of subscriptions within cloud tenant: %s.' % len(children_cloud_accounts))

tenants_childrens_creds = get_tenant_children_creds(
                                                    compute_credential_list,
                                                    tenant_client_info['cloudAccount']['name']
                                                   )
print('INFO  - Number of existing compute credentials belonging to tenant: %s.'
      % len(tenants_childrens_creds))

deleted_count = del_orphaned_credentials(tenants_childrens_creds, children_cloud_accounts)
added_count = add_missing_credentials(tenants_childrens_creds, children_cloud_accounts, args.clientId)

print('Total Added   : %s' %added_count)
print('Total Deleted : %s' %deleted_count)
