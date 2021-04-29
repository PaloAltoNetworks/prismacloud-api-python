import json
import requests
import time
import pc_lib_general

# --Description-- #

# Prisma Cloud API Helper library. Contains shared API functions.

# --Helper Methods-- #

class PrismaCloudAPI(object):
    def __init__(self):
        self.api           = None
        self.username      = None
        self.password      = None
        self.token         = None
        self.token_timer   = 0
        self.token_limit   = 540
        self.retry_limit   = 3
        self.retry_pause   = 5
        self.retry_status_codes = [401, 429, 500, 502, 503, 504]

    def configure(self, api, username, password):
        self.api      = api
        self.username = username
        self.password = password

    def login(self):
        requ_url = 'https://%s/login' % self.api
        requ_action = 'POST'
        requ_headers = {'Content-Type': 'application/json'}
        requ_data = json.dumps({'username': self.username, 'password': self.password})
        api_response = requests.request(requ_action, requ_url, headers=requ_headers, data=requ_data)
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token') 
            self.token_timer = time.time()
        else:
            pc_lib_general.pc_exit_error(api_response.status_code, 'The API (login) returned an unexpected response:\n%s' % api_response.content)

    def extend_token(self):
        requ_url = 'https://%s/auth_token/extend' % self.api
        requ_action = 'GET'
        requ_headers = {'Content-Type': 'application/json', 'x-redlock-auth': self.token}
        api_response = requests.request(requ_action, requ_url, headers=requ_headers)
        if api_response.status_code in self.retry_status_codes:
            for retry_number in range(1, self.retry_limit):
                time.sleep(self.retry_pause)
                api_response = requests.request(requ_action, requ_url, headers=requ_headers)
                if api_response.ok:
                    break
        if api_response.ok:
            self.token_timer = time.time() 
        else:
            pc_lib_general.pc_exit_error(api_response.status_code, 'The API (extend) returned an unexpected response.')

    def execute(self, action, endpoint, query_params=None, body_params=None):
        if not self.token:
            self.login()
        if int(time.time() - self.token_timer) > self.token_limit:
            self.extend_token()
        requ_url = 'https://%s/%s' % (self.api, endpoint)
        requ_action = action
        requ_headers = {'Content-Type': 'application/json'}
        if self.token:
            requ_headers['x-redlock-auth'] = self.token
        requ_data = json.dumps(body_params)
        api_response = requests.request(requ_action, requ_url, headers=requ_headers)
        if api_response.status_code in self.retry_status_codes:
            for retry_number in range(1, self.retry_limit):
                time.sleep(self.retry_pause)
                api_response = requests.request(requ_action, requ_url, headers=requ_headers)
                if api_response.ok:
                    break
        if api_response.ok:
            try:
                result = json.loads(api_response.content)
            except ValueError:
                if api_response.content == '':
                   result = None
        else:
            pc_lib_general.pc_exit_error(api_response.status_code, 'The API (execute) returned an unexpected response:\n%s' % api_response.content)
        return result

pc_api = PrismaCloudAPI()

# --Action Methods-- #

def current_user():
    return pc_api.execute('GET', 'user/me')

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

def api_compliance_standard_list_get():
    return pc_api.execute('GET', 'compliance')

def api_compliance_standard_add(compliance_standard_to_add):
    return pc_api.execute('POST', 'compliance', body_params=compliance_standard_to_add)

def api_compliance_standard_get(compliance_standard_id):
    return pc_api.execute('GET', 'compliance/%s' % compliance_standard_id)

def api_compliance_standard_delete(compliance_standard_id):
    return pc_api.execute('DELETE', 'compliance/%s' % compliance_standard_id)

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

def api_compliance_standard_requirement_list_get(compliance_standard_id):
    return pc_api.execute('GET', 'compliance/%s/requirement' % compliance_standard_id)

def api_compliance_standard_requirement_add(compliance_standard_id, compliance_requirement_to_add):
    return pc_api.execute('POST', 'compliance/%s/requirement' % compliance_standard_id, body_params=compliance_requirement_to_add)

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

def api_compliance_standard_requirement_section_list_get(compliance_requirement_id):
    return pc_api.execute('GET', 'compliance/%s/section' % compliance_requirement_id)

def api_compliance_standard_requirement_section_add(compliance_requirement_id, compliance_section_to_add):
    return pc_api.execute('POST', 'compliance/%s/section' % compliance_requirement_id, body_params=compliance_section_to_add)

"""
  ComplianceStandards Requirements Policies

[x] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[ ] DELETE/REMOVE
Additional:
[x] LIST (v2)

"""

def api_compliance_standard_policy_list_get(compliance_standard_name):
    filters = [('policy.complianceStandard', compliance_standard_name)]
    return pc_api.execute('GET', 'policy', query_params=filters)

def api_compliance_standard_policy_v2_list_get(compliance_standard_name):
    filters = [('policy.complianceStandard', compliance_standard_name)]
    return pc_api.execute('GET', 'v2/policy', query_params=filters)

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

def api_policy_list_get():
    return pc_api.execute('GET', 'policy')

def api_policy_v2_list_get():
    return pc_api.execute('GET', 'v2/policy')

def api_policy_custom_v2_list_get():
    filters = [('policy.policyMode', 'custom')]
    return pc_api.execute('GET', 'v2/policy', query_params=filters)

def api_policy_add(policy_to_add):
    return pc_api.execute('POST', 'policy', body_params=policy_to_add)

def api_policy_get(policy_id):
    return pc_api.execute('GET', 'policy/%s' % policy_id)

def api_policy_update(policy_id, policy_update):
    return pc_api.execute('PUT', 'policy/%s' % policy_id, body_params=policy_update)

def api_policy_status_update(policy_id, policy_status_update):
    return pc_api.execute('PATCH', 'policy/%s/status/%s' % (policy_id, policy_status_update))

def api_policy_delete(policy_id):
    return pc_api.execute('DELETE', 'policy/%s' % policy_id)

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

def api_saved_search_list_get():
    return pc_api.execute('GET', 'search/history?filter=saved')

def api_saved_search_add(type_of_search, saved_search_to_add):
    if type_of_search == 'network':
        return pc_api.execute('POST', 'search', body_params=saved_search_to_add)
    else:
        return pc_api.execute('POST', 'search/%s' % type_of_search, body_params=saved_search_to_add)

def api_saved_search_get(saved_search_id):
    return pc_api.execute('GET', 'search/history/%s' % saved_search_id)

def api_saved_search_delete(saved_search_id):
    return pc_api.execute('DELETE', 'search/history/%s' % saved_search_id)

"""
  User Roles

[x] LIST
[ ] CREATE/ADD
[x] READ/GET
[x] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[ ] As above with restrictions/filtering
"""

def api_user_role_list_get():
    return pc_api.execute('GET', 'user/role')

def api_user_role_add(user_role_to_add):
    return pc_api.execute('POST', 'user/role', body_params=user_role_to_add)

def api_user_role_update(user_role_id, user_role_update):
    return pc_api.execute('PUT', 'user/role/%s' % user_role_id, body_params=user_role_update)

def api_user_role_get(user_role_id):
    return pc_api.execute('GET', 'user/role/%s' % user_role_id)

def api_user_role_delete(user_role_id):
    return pc_api.execute('DELETE', 'user/role/%s' % user_role_id)

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

def api_user_list_get():
    return pc_api.execute('GET', 'user')

def api_user_list_get_v2():
    return pc_api.execute('GET', 'v2/user')

def api_user_add(user_to_add):
    return pc_api.execute('POST', 'user', body_params=user_to_add)

def api_user_get(user_email):
    return pc_api.execute('GET', 'user/%s' % user_email)

# TODO: Use this model for other updates?

def api_user_update(user_to_update):
    return pc_api.execute('PUT', 'user/%s' % user_to_update['email'], body_params=user_to_update)

"""
  Alerts

[x] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[ ] DELETE/REMOVE
Additional:
[x] LIST v2
"""

def api_alert_list_get(qp=None, bp=None):
    return pc_api.execute('POST', 'alert', query_params=qp, body_params=bp)

def api_alert_v2_list_get(qp=None, bp=None):
    return pc_api.execute('POST', 'v2/alert', query_params=qp, body_params=bp)

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

def api_compliance_report_list_get():
    return pc_api.execute('GET', 'report')

def api_compliance_report_add(report_to_add):
    return pc_api.execute('POST', 'report', body_params=report_to_add)

def api_compliance_report_delete(report_id):
    return pc_api.execute('DELETE', 'report/%s' % report_id)

def api_compliance_report_download(report_id):
    return pc_api.execute('GET', 'report/%s/download' % report_id)
    # TODO: 
    #if response_status == 204:
    #    # download pending
    #    pass
    #elif response_status == 200:
    #    # download ready
    #    pass
    #else:

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

def api_cloud_accounts_list_get(qp=None):
    return pc_api.execute('GET', 'cloud', query_params=qp)

def api_cloud_accounts_list_names_get(qp=None):
    return pc_api.execute('GET', 'cloud/name', query_params=qp)

def api_cloud_accounts_add(cloud_type, cloud_account_to_add):
    return pc_api.execute('POST', 'cloud/%s' % cloud_type, body_params=cloud_account_to_add)

def api_cloud_account_update(cloud_type, cloud_account_id, cloud_account_update):
    return pc_api.execute('PUT', 'cloud/%s/%s' % (cloud_type, cloud_account_id), body_params=cloud_account_update)

def api_cloud_account_delete(cloud_type, cloud_account_id):
    return pc_api.execute('DELETE', 'cloud/%s/%s' % (cloud_type, cloud_account_id))

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

def api_cloud_account_group_list_get():
    return pc_api.execute('GET', 'cloud/group')

def api_cloud_account_group_add(cloud_account_group_to_add):
    return pc_api.execute('POST', 'cloud/group', body_params=cloud_account_group_to_add)

def api_cloud_account_group_get(cloud_account_group_id):
    return pc_api.execute('GET', 'cloud/group/%s' % cloud_account_group_id)

def api_cloud_account_group_update(cloud_account_group_id, cloud_account_group_update):
    return pc_api.execute('PUT', 'cloud/group/%s' % cloud_account_group_id, body_params=cloud_account_group_update)

def api_cloud_account_group_delete(cloud_account_group_id):
    return pc_api.execute('DELETE', 'cloud/group/%s' % cloud_account_group_id)

"""
  Alert Rules

[x] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[x] LIST v2
"""

def api_alert_rule_list_get():
    return pc_api.execute('GET', 'v2/alert/rule')

def api_alert_rule_delete(alert_rule_id):
    return pc_api.execute('DELETE', 'alert/rule/%s' % alert_rule_id)

"""
  Integration Lists

[x] LIST
[ ] CREATE/ADD
[ ] READ/GET
[ ] UPDATE/REPLACE
[x] DELETE/REMOVE
Additional:
[ ] LIST v2
"""

def api_integration_list_get():
    return pc_api.execute('GET', 'integration')

def api_integration_delete(integration_id):
    return pc_api.execute('DELETE', 'integration/%s' % integration_id)

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

def api_resource_list_list_get():
    # TODO: Does this require ?listType=TAG
    return pc_api.execute('GET', 'v1/resource_list')

def api_resource_list_delete(resource_list_id):
    return pc_api.execute('DELETE', 'v1/resource_list/%s' % resource_list_id)

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

def api_access_keys_list_get():
    return pc_api.execute('GET', 'access_keys')

def api_access_key_add(access_key_to_add):
    return pc_api.execute('POST', 'access_keys', body_params=access_key_to_add)

def api_access_key_get(access_key_id):
    return pc_api.execute('GET', 'access_keys' % access_key_id)

def api_access_key_update(access_key_id, access_key_update):
    return pc_api.execute('PUT', 'access_keys/%s' % access_key_id, body_params=access_key_update)

# Note: Expired keys cannot be enabled.
def api_access_key_status_update(access_key_id, access_key_status):
    return pc_api.execute('PATCH', 'access_keys/%s/status/%s' % (access_key_id, access_key_status))

def api_access_key_delete(access_key_id):
    return pc_api.execute('DELETE', 'access_keys/%s' % access_key_id)
