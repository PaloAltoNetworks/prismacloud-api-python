import json
import requests
import time
import pc_lib_general

# --Description-- #

# Prisma Cloud API Helper library. Contains shared API functions.

# --Helper Methods-- #

def pc_call_api(action, api_url, pc_settings, data=None, params=None, retry_count=0, max_retries=3, auth_retry_count=0, auth_max_retries=3):
    auth_retry_statuses = [401]
    retry_statuses      = [429, 500, 502, 503, 504]
    retry_wait_timer    = 5
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': pc_settings['jwt']}
    response = requests.request(action, api_url, params=params, headers=headers, data=json.dumps(data))
    # Check for an error to retry, re-authenticate, or fail.
    if response.status_code in retry_statuses:
        retry_count = retry_count + 1
        if retry_count <= max_retries:
            time.sleep(retry_wait_timer)
            return pc_call_api(action=action, api_url=api_url, pc_settings=pc_settings, data=data, params=params, retry_count=retry_count, max_retries=max_retries, auth_retry_count=auth_retry_count, auth_max_retries=auth_max_retries)
        else:
            response.raise_for_status()
    elif response.status_code in auth_retry_statuses and pc_settings['jwt'] is not None:
        auth_retry_count = auth_retry_count + 1
        if auth_retry_count <= auth_max_retries:
            pc_settings = pc_login(pc_settings)
            return pc_call_api(action=action, api_url=api_url, pc_settings=pc_settings, data=data, params=params, retry_count=retry_count, max_retries=max_retries, auth_retry_count=auth_retry_count, auth_max_retries=auth_max_retries)
        else:
            response.raise_for_status()
    else:
        response.raise_for_status()
    # Check for valid response, and catch if empty, none, or otherwise unexpected.
    api_response_package = {}
    api_response_package['statusCode'] = response.status_code
    try:
        api_response_package['data'] = response.json()
    except ValueError:
        if response.text == '':
            api_response_package['data'] = None
        else:
            pc_lib_general.pc_exit_error(501, 'The API returned an unexpected response.')
    return pc_settings, api_response_package


def pc_login(pc_settings):
    url = "https://" + pc_settings['apiBase'] + "/login"
    action = "POST"
    pc_settings['jwt'] = pc_call_api(action, url, pc_settings, data=pc_settings)[1]['data']['token']
    return pc_settings

# --Action Methods-- #

"""
  Note: Eventually, all objects covered should have full CRUD capability, ie, to create, read, update, and delete (and list)

  Template:

[ ] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[ ] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""

# Main API Actions

"""
  ComplianceStandards

[x] LIST
[x] CREATE/ADD
[x] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""

def api_compliance_standard_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/compliance"
    return pc_call_api(action, url, pc_settings)


def api_compliance_standard_add(pc_settings, compliance_standard_new):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/compliance"
    return pc_call_api(action, url, pc_settings, data=compliance_standard_new)

def api_compliance_standard_get(pc_settings, compliance_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_id
    return pc_call_api(action, url, pc_settings)

def api_compliance_standard_delete(pc_settings, compliance_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_id
    return pc_call_api(action, url, pc_settings)


"""
  ComplianceStandards Requirements

[x] LIST
[x] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[ ] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""

def api_compliance_standard_requirement_list_get(pc_settings, compliance_standard_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_standard_id + "/requirement"
    return pc_call_api(action, url, pc_settings)


def api_compliance_standard_requirement_add(pc_settings, compliance_standard_id, compliance_requirement_new):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_standard_id + "/requirement"
    return pc_call_api(action, url, pc_settings, data=compliance_requirement_new)


"""
  ComplianceStandards Requirements Sections

[x] LIST
[x] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[ ] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""

def api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_requirement_id + "/section"
    return pc_call_api(action, url, pc_settings)


def api_compliance_standard_requirement_section_add(pc_settings, compliance_requirement_id, compliance_section_new):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_requirement_id + "/section"
    return pc_call_api(action, url, pc_settings, data=compliance_section_new)

"""
  ComplianceStandards Requirements Policies

[x] LIST
[x] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[ ] DELETE/REMOVE
Additional:
[x] LIST (v2)

"""

def api_compliance_standard_policy_list_get(pc_settings, source_compliance_standard_name):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/policy"
    filters = [('policy.complianceStandard', source_compliance_standard_name)]
    return pc_call_api(action, url, pc_settings, params=filters)


def api_compliance_standard_policy_v2_list_get(pc_settings, source_compliance_standard_name):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/policy"
    filters = [('policy.complianceStandard', source_compliance_standard_name)]
    return pc_call_api(action, url, pc_settings, params=filters)

"""
  Policies

[x] LIST
[x] CREATE/ADD
[x] READ/GET
[x] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[x] LIST v2
[x] LIST v2 where custom
[x] UPDATE status
"""


def api_policy_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/policy"
    return pc_call_api(action, url, pc_settings)


def api_policy_v2_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/policy"
    return pc_call_api(action, url, pc_settings)


def api_policy_custom_v2_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/policy"
    filters = [('policy.policyMode', 'custom')]
    return pc_call_api(action, url, pc_settings, params=filters)


def api_policy_add(pc_settings, policy_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/policy"
    return pc_call_api(action, url, pc_settings, data=policy_to_add)


def api_policy_get(pc_settings, policy_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/policy/" + policy_id
    return pc_call_api(action, url, pc_settings)


def api_policy_update(pc_settings, policy_id, policy_update):
    action = "PUT"
    url = "https://" + pc_settings['apiBase'] + "/policy/" + policy_id
    return pc_call_api(action, url, pc_settings, data=policy_update)


def api_policy_status_update(pc_settings, policy_id, status):
    action = "PATCH"
    url = "https://" + pc_settings['apiBase'] + "/policy/" + policy_id + "/status/" + status
    return pc_call_api(action, url, pc_settings)


def api_policy_delete(pc_settings, policy_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/policy/" + policy_id
    return pc_call_api(action, url, pc_settings)

"""
  Search

[x] LIST
[x] CREATE/ADD
[x] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""


def api_saved_search_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/search/history?filter=saved"
    return pc_call_api(action, url, pc_settings)


def api_search_add(pc_settings, type_of_search, search_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/search/" + type_of_search
    if type_of_search=='network':
        url="https://" + pc_settings['apiBase'] + "/search"
    return pc_call_api(action, url, pc_settings, data=search_to_add)


def api_search_get(pc_settings, search_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/search/history/" + search_id
    return pc_call_api(action, url, pc_settings)


def api_saved_search_delete(pc_settings, search_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/search/history/" + search_id
    return pc_call_api(action, url, pc_settings)


"""
  User Roles

[x] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""

def api_user_role_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/user/role"
    return pc_call_api(action, url, pc_settings)


def api_user_role_add(pc_settings, user_role_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/user/role"
    return pc_call_api(action, url, pc_settings, data=user_role_to_add)


def api_user_role_update(pc_settings, user_role_to_update, user_role_update):
    action = "PUT"
    url = "https://" + pc_settings['apiBase'] + "/user/role/" + user_role_to_update
    return pc_call_api(action, url, pc_settings, data=user_role_update)


def api_user_role_get(pc_settings, user_role_to_get):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/user/role/" + user_role_to_get
    return pc_call_api(action, url, pc_settings)


def api_user_role_delete(pc_settings, account_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/user/role/" + id
    return pc_call_api(action, url, pc_settings)

"""
  Users

[x] LIST
[x] CREATE/ADD
[x] READ/GET
[x] UPDATE/REPLACE
[ ] DELETE/REMOVE
Additional:
[x] LIST v2
"""

def api_user_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/user"
    return pc_call_api(action, url, pc_settings)


def api_user_list_get_v2(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/user"
    return pc_call_api(action, url, pc_settings)


def api_user_add(pc_settings, user_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/user"
    return pc_call_api(action, url, pc_settings, data=user_to_add)


def api_user_get(pc_settings, useremail):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/user/" + useremail
    return pc_call_api(action, url, pc_settings)


def api_user_update(pc_settings, user_to_update):
    action = "PUT"
    url = "https://" + pc_settings['apiBase'] + "/user/" + user_to_update['email']
    return pc_call_api(action, url, pc_settings, data=user_to_update)


"""
  Alerts

[x] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[x] LIST v2
"""

def api_alert_list_get(pc_settings, params=None, data=None):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/alert"
    return pc_call_api(action, url, pc_settings, params=params, data=data)


def api_alert_v2_list_get(pc_settings, params=None, data=None):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/v2/alert"
    return pc_call_api(action, url, pc_settings, params=params, data=data)


"""
  Compliance Reports

[x] LIST
[x] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[x] DOWNLOAD
"""

def api_compliance_report_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/report"
    return pc_call_api(action, url, pc_settings)


def api_compliance_report_add(pc_settings, report_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/report"
    return pc_call_api(action, url, pc_settings, data=report_to_add)


def api_compliance_report_delete(pc_settings, report_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/report/" + report_id
    return pc_call_api(action, url, pc_settings)


def api_compliance_report_download(pc_settings, report_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/report/" + report_id + "/download"
    jwt, response_status, response_json = pc_call_api(action, url, pc_settings)
    if response_status == 204:
        # download pending
        pass
    elif response_status == 200:
        # download ready
        pass


"""
  Cloud Accounts

[x] LIST
[x] CREATE/ADD
[ ] READ/GET
[x] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[x] LIST names
"""

def api_cloud_accounts_list_get(pc_settings, params=None):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/cloud"
    return pc_call_api(action, url, pc_settings, params=params)


def api_cloud_accounts_list_names_get(pc_settings, params=None):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/cloud/name"
    return pc_call_api(action, url, pc_settings, params=params)


def api_cloud_accounts_add(pc_settings, cloud_type, cloud_account_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/cloud/" + cloud_type
    return pc_call_api(action, url, pc_settings, data=cloud_account_to_add)


def api_cloud_account_update(pc_settings, cloud_type, cloud_account_to_update, cloud_account_update):
    action = "PUT"
    url = "https://" + pc_settings['apiBase'] + "/cloud/" + cloud_type + "/" + cloud_account_to_update
    return pc_call_api(action, url, pc_settings, data=cloud_account_update)


def api_cloud_account_delete(pc_settings, account_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/cloud/" + account_id
    return pc_call_api(action, url, pc_settings)


"""
  Cloud Account Groups

[x] LIST
[x] CREATE/ADD
[x] READ/GET
[x] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""

def api_cloud_account_group_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/cloud/group"
    return pc_call_api(action, url, pc_settings)


def api_account_group_add(pc_settings, account_group_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/cloud/group"
    return pc_call_api(action, url, pc_settings, data=account_group_to_add)


def api_account_group_get(pc_settings, account_group_to_get):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/cloud/group/" + account_group_to_get
    return pc_call_api(action, url, pc_settings)


def api_account_group_update(pc_settings, account_group_to_update, account_group_update):
    action = "PUT"
    url = "https://" + pc_settings['apiBase'] + "/cloud/group/" + account_group_to_update
    return pc_call_api(action, url, pc_settings, data=account_group_update)


def api_cloud_account_group_delete(pc_settings, group_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/cloud/group/" + group_id
    return pc_call_api(action, url, pc_settings)

"""
  Alert Rules

[ ] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[x] LIST v2
"""

def api_alert_rule_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/alert/rule"
    return pc_call_api(action, url, pc_settings)


def api_alert_rule_delete(pc_settings, rule_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/alert/rule/" + rule_id
    return pc_call_api(action, url, pc_settings)


"""
  Integration Lists

[ ] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[x] LIST v2
"""

def api_integration_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/integration"
    return pc_call_api(action, url, pc_settings)


def api_integration_delete(pc_settings, integration_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/integration/" + integration_id
    return pc_call_api(action, url, pc_settings)


"""
  Resource Lists

[x] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""

def api_resource_list_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v1/resource_list"
    return pc_call_api(action, url, pc_settings)


def api_resource_list_delete(pc_settings, resource_list_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/v1/resource_list/" + resource_list_id
    return pc_call_api(action, url, pc_settings)


"""
  Access Keys

[x] LIST
[x] CREATE/ADD
[x] READ/GET
[x] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[x] UPDATE status
"""

def api_access_keys_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/access_keys"
    return pc_call_api(action, url, pc_settings)


def api_access_key_add(pc_settings, access_key_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/access_keys"
    return pc_call_api(action, url, pc_settings, data=access_key_to_add)


def api_access_key_by_id_get(pc_settings, access_key_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/access_keys/" + access_key_id
    return pc_call_api(action, url, pc_settings)


def api_access_key_update(pc_settings, access_key_to_update, access_key_values):
    action = "PUT"
    url = "https://" + pc_settings['apiBase'] + "/access_keys/" + access_key_to_update
    return pc_call_api(action, url, pc_settings, data=access_key_values)


# Note: Expired keys cannot be enabled.
def api_access_key_status_update(pc_settings, access_key_to_update, access_key_status):
    action = "PATCH"
    url = "https://" + pc_settings['apiBase'] + "/access_keys/" + access_key_to_update + "/status/status"
    return pc_call_api(action, url, pc_settings, data=access_key_status)


def api_access_key_delete(pc_settings, access_key_to_delete):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/access_keys/" + access_key_to_delete
    return pc_call_api(action, url, pc_settings)
