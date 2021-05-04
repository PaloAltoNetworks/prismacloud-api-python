from __future__ import print_function

from .pc_lib_api_extended import PrismaCloudAPIExtended
from .pc_lib_utility import PrismaCloudUtility

import json
import requests
import time

# --Description-- #

# Prisma Cloud API library.

# --Class Methods-- #

class PrismaCloudAPI(PrismaCloudAPIExtended):
    def __init__(self):
        self.api                = None
        self.username           = None
        self.password           = None
        self.ca_bundle          = None
        self.token              = None
        self.token_timer        = 0
        self.token_limit        = 540
        self.retry_limit        = 3
        self.retry_pause        = 5
        self.retry_status_codes = [401, 429, 500, 502, 503, 504]
        self.max_workers        = 16

    def configure(self, settings):
        self.api       = settings['apiBase']
        self.username  = settings['username']
        self.password  = settings['password']
        self.ca_bundle = settings['ca_bundle']

    def login(self):
        requ_url = 'https://%s/login' % self.api
        requ_action = 'POST'
        requ_headers = {'Content-Type': 'application/json'}
        requ_data = json.dumps({'username': self.username, 'password': self.password})
        api_response = requests.request(requ_action, requ_url, headers=requ_headers, data=requ_data, verify=self.ca_bundle)
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token') 
            self.token_timer = time.time()
        else:
            PrismaCloudUtility.error_and_exit(api_response.status_code, 'The API (login) returned an unexpected response:\n%s' % api_response.text)

    def extend_token(self):
        requ_url = 'https://%s/auth_token/extend' % self.api
        requ_action = 'GET'
        requ_headers = {'Content-Type': 'application/json', 'x-redlock-auth': self.token}
        api_response = requests.request(requ_action, requ_url, headers=requ_headers, verify=self.ca_bundle)
        if api_response.status_code in self.retry_status_codes:
            for retry_number in range(1, self.retry_limit):
                time.sleep(self.retry_pause)
                api_response = requests.request(requ_action, requ_url, headers=requ_headers, verify=self.ca_bundle)
                if api_response.ok:
                    break
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token') 
            self.token_timer = time.time() 
        else:
            PrismaCloudUtility.error_and_exit(api_response.status_code, 'The API (extend) returned an unexpected response:\n%s' % api_response.text)

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
        requ_params = query_params
        requ_data = json.dumps(body_params)
        api_response = requests.request(requ_action, requ_url, headers=requ_headers, params=requ_params, data=requ_data, verify=self.ca_bundle)
        if api_response.status_code in self.retry_status_codes:
            for retry_number in range(1, self.retry_limit):
                time.sleep(self.retry_pause)
                api_response = requests.request(requ_action, requ_url, headers=requ_headers, params=query_params, data=requ_data, verify=self.ca_bundle)
                if api_response.ok:
                    break
        if api_response.ok:
            try:
                result = json.loads(api_response.content)
            except ValueError:
                if api_response.content == '':
                   result = None
        else:
            PrismaCloudUtility.error_and_exit(api_response.status_code, 'The API (%s) returned an unexpected response:\n%s' % (endpoint, api_response.text))
        return result

    def progress(self, output='', optional=False):
        if not optional:
            print(output)

    # --API Endpoints-- #

    def current_user(self):
            return self.execute('GET', 'user/me')

    """
    Note: Eventually, all objects covered should have full CRUD capability, ie, to create, read, update, and delete (and list).

    Template

    [ ] LIST
    [ ] CREATE/ADD
    [ ] READ/GET
    [ ] UPDATE/REPLACE
    [ ] DELETE/REMOVE
    Additional:
    [ ] As above with restrictions/filtering
    """

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

    def alert_list_get(self, qp=None, bp=None):
        return self.execute('POST', 'alert', query_params=qp, body_params=bp)

    def alert_v2_list_get(self, qp=None, bp=None):
        return self.execute('POST', 'v2/alert', query_params=qp, body_params=bp)

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

    def policy_list_get(self):
        return self.execute('GET', 'policy')

    def policy_v2_list_get(self):
        return self.execute('GET', 'v2/policy')

    def policy_custom_v2_list_get(self):
        filters = [('policy.policyMode', 'custom')]
        return self.execute('GET', 'v2/policy', query_params=filters)

    def policy_add(self, policy_to_add):
        return self.execute('POST', 'policy', body_params=policy_to_add)

    def policy_get(self, policy_id):
        return self.execute('GET', 'policy/%s' % policy_id)

    def policy_update(self, policy_id, policy_update):
        return self.execute('PUT', 'policy/%s' % policy_id, body_params=policy_update)

    def policy_status_update(self, policy_id, policy_status_update):
        return self.execute('PATCH', 'policy/%s/status/%s' % (policy_id, policy_status_update))

    def policy_delete(self, policy_id):
        return self.execute('DELETE', 'policy/%s' % policy_id)

    """
    Saved Searches

    [x] LIST
    [x] CREATE/ADD
    [x] READ/GET
    [ ] UPDATE/REPLACE
    [x] DELETE/REMOVE
    Additional:
    [ ] As above with restrictions/filtering
    """

    def saved_search_list_get(self):
        return self.execute('GET', 'search/history?filter=saved')

    def saved_search_add(self, type_of_search, saved_search_to_add):
        if type_of_search == 'network':
            return self.execute('POST', 'search', body_params=saved_search_to_add)
        else:
            return self.execute('POST', 'search/%s' % type_of_search, body_params=saved_search_to_add)

    def saved_search_get(self, saved_search_id):
        return self.execute('GET', 'search/history/%s' % saved_search_id)

    def saved_search_delete(self, saved_search_id):
        return self.execute('DELETE', 'search/history/%s' % saved_search_id)

    """
    Compliance Standards

    [x] LIST
    [x] CREATE/ADD
    [x] READ/GET
    [ ] UPDATE/REPLACE
    [x] DELETE/REMOVE
    Additional:
    [ ] As above with restrictions/filtering
    """

    def compliance_standard_list_get(self):
        return self.execute('GET', 'compliance')

    def compliance_standard_add(self, compliance_standard_to_add):
        return self.execute('POST', 'compliance', body_params=compliance_standard_to_add)

    def compliance_standard_get(self, compliance_standard_id):
        return self.execute('GET', 'compliance/%s' % compliance_standard_id)

    def compliance_standard_delete(self, compliance_standard_id):
        return self.execute('DELETE', 'compliance/%s' % compliance_standard_id)

    """
    Compliance Standard Requirements

    [x] LIST
    [x] CREATE/ADD
    [ ] READ/GET
    [ ] UPDATE/REPLACE
    [ ] DELETE/REMOVE
    Additional:
    [ ] As above with restrictions/filtering
    """

    def compliance_standard_requirement_list_get(self, compliance_standard_id):
        return self.execute('GET', 'compliance/%s/requirement' % compliance_standard_id)

    def compliance_standard_requirement_add(self, compliance_standard_id, compliance_requirement_to_add):
        return self.execute('POST', 'compliance/%s/requirement' % compliance_standard_id, body_params=compliance_requirement_to_add)

    """
    Compliance Standard Requirements Sections

    [x] LIST
    [x] CREATE/ADD
    [ ] READ/GET
    [ ] UPDATE/REPLACE
    [ ] DELETE/REMOVE
    Additional:
    [ ] As above with restrictions/filtering
    """

    def compliance_standard_requirement_section_list_get(self, compliance_requirement_id):
        return self.execute('GET', 'compliance/%s/section' % compliance_requirement_id)

    def compliance_standard_requirement_section_add(self, compliance_requirement_id, compliance_section_to_add):
        return self.execute('POST', 'compliance/%s/section' % compliance_requirement_id, body_params=compliance_section_to_add)

    """
    Compliance Standard Requirements Policies

    [x] LIST
    [ ] CREATE/ADD
    [ ] READ/GET
    [ ] UPDATE/REPLACE
    [ ] DELETE/REMOVE
    Additional:
    [x] LIST (v2)

    """

    def compliance_standard_policy_list_get(self, compliance_standard_name):
        filters = [('policy.complianceStandard', compliance_standard_name)]
        return self.execute('GET', 'policy', query_params=filters)

    def compliance_standard_policy_v2_list_get(self, compliance_standard_name):
        filters = [('policy.complianceStandard', compliance_standard_name)]
        return self.execute('GET', 'v2/policy', query_params=filters)

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

    def user_list_get(self):
        return self.execute('GET', 'user')

    def user_list_get_v2(self):
        return self.execute('GET', 'v2/user')

    def user_add(self, user_to_add):
        return self.execute('POST', 'user', body_params=user_to_add)

    def user_get(self, user_email):
        return self.execute('GET', 'user/%s' % user_email)

    # TODO: Use this model for other updates?

    def user_update(self, user_to_update):
        return self.execute('PUT', 'user/%s' % user_to_update['email'], body_params=user_to_update)

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

    def user_role_list_get(self):
        return self.execute('GET', 'user/role')

    def user_role_add(self, user_role_to_add):
        return self.execute('POST', 'user/role', body_params=user_role_to_add)

    def user_role_update(self, user_role_id, user_role_update):
        return self.execute('PUT', 'user/role/%s' % user_role_id, body_params=user_role_update)

    def user_role_get(self, user_role_id):
        return self.execute('GET', 'user/role/%s' % user_role_id)

    def user_role_delete(self, user_role_id):
        return self.execute('DELETE', 'user/role/%s' % user_role_id)

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

    def access_keys_list_get(self):
        return self.execute('GET', 'access_keys')

    def access_key_add(self, access_key_to_add):
        return self.execute('POST', 'access_keys', body_params=access_key_to_add)

    def access_key_get(self, access_key_id):
        return self.execute('GET', 'access_keys' % access_key_id)

    def access_key_update(self, access_key_id, access_key_update):
        return self.execute('PUT', 'access_keys/%s' % access_key_id, body_params=access_key_update)

    # Note: Expired keys cannot be enabled.
    def access_key_status_update(self, access_key_id, access_key_status):
        return self.execute('PATCH', 'access_keys/%s/status/%s' % (access_key_id, access_key_status))

    def access_key_delete(self, access_key_id):
        return self.execute('DELETE', 'access_keys/%s' % access_key_id)

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

    def cloud_accounts_list_get(self, qp=None):
        return self.execute('GET', 'cloud', query_params=qp)

    def cloud_accounts_list_names_get(self, qp=None):
        return self.execute('GET', 'cloud/name', query_params=qp)

    def cloud_accounts_add(self, cloud_type, cloud_account_to_add):
        return self.execute('POST', 'cloud/%s' % cloud_type, body_params=cloud_account_to_add)

    def cloud_account_update(self, cloud_type, cloud_account_id, cloud_account_update):
        return self.execute('PUT', 'cloud/%s/%s' % (cloud_type, cloud_account_id), body_params=cloud_account_update)

    def cloud_account_delete(self, cloud_type, cloud_account_id):
        return self.execute('DELETE', 'cloud/%s/%s' % (cloud_type, cloud_account_id))

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

    def cloud_account_group_list_get(self):
        return self.execute('GET', 'cloud/group')

    def cloud_account_group_add(self, cloud_account_group_to_add):
        return self.execute('POST', 'cloud/group', body_params=cloud_account_group_to_add)

    def cloud_account_group_get(self, cloud_account_group_id):
        return self.execute('GET', 'cloud/group/%s' % cloud_account_group_id)

    def cloud_account_group_update(self, cloud_account_group_id, cloud_account_group_update):
        return self.execute('PUT', 'cloud/group/%s' % cloud_account_group_id, body_params=cloud_account_group_update)

    def cloud_account_group_delete(self, cloud_account_group_id):
        return self.execute('DELETE', 'cloud/group/%s' % cloud_account_group_id)

    """
    Asset (Resources) Inventory

    [x] LIST
    [ ] CREATE/ADD
    [ ] READ/GET
    [ ] UPDATE/REPLACE
    [ ] DELETE/REMOVE
    Additional:
    [x] LIST v2
    """

    def asset_inventory_list_get(self, qp=None):
        return self.execute('GET', 'v2/inventory', query_params=qp)

    """
    (Assets) Resources

    [ ] LIST
    [ ] CREATE/ADD
    [x] READ/GET
    [ ] UPDATE/REPLACE
    [ ] DELETE/REMOVE
    """

    def resource_get(self, bp=None):
        return self.execute('POST', 'resource', body_params=bp)

    def resource_timeline_get(self, bp=None):
        return self.execute('POST', 'resource/timeline', body_params=bp)

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

    def alert_rule_list_get(self):
        return self.execute('GET', 'v2/alert/rule')

    def alert_rule_delete(self, alert_rule_id):
        return self.execute('DELETE', 'alert/rule/%s' % alert_rule_id)

    """
    Integrations

    [x] LIST
    [ ] CREATE/ADD
    [ ] READ/GET
    [ ] UPDATE/REPLACE
    [x] DELETE/REMOVE
    Additional:
    [ ] LIST v2
    """

    def integration_list_get(self):
        return self.execute('GET', 'integration')

    def integration_delete(self, integration_id):
        return self.execute('DELETE', 'integration/%s' % integration_id)

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

    def resource_list_list_get(self):
        # TODO: Does this require ?listType=TAG
        return self.execute('GET', 'v1/resource_list')

    def resource_list_delete(self, resource_list_id):
        return self.execute('DELETE', 'v1/resource_list/%s' % resource_list_id)

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

    def compliance_report_list_get(self):
        return self.execute('GET', 'report')

    def compliance_report_add(self, report_to_add):
        return self.execute('POST', 'report', body_params=report_to_add)

    def compliance_report_delete(self, report_id):
        return self.execute('DELETE', 'report/%s' % report_id)

    def compliance_report_download(self, report_id):
        return self.execute('GET', 'report/%s/download' % report_id)
        # TODO: 
        #if response_status == 204:
        #    # download pending
        #    pass
        #elif response_status == 200:
        #    # download ready
        #    pass
        #else:
