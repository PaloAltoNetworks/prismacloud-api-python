import json
import requests
import time
import pc_lib_general


# --Description-- #
# Prisma Cloud API Helper library.  Contains shared API call functions.
# --End Description-- #


# --Helper Methods-- #
# Main API Call Function
def pc_call_api(action, api_url, pc_settings, data=None, params=None, try_count=0, max_retries=2, auth_count=0, auth_retries=1):
    retry_statuses = [429, 500, 502, 503, 504]
    auth_statuses = [401]
    retry_wait_timer = 5
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': pc_settings['jwt']}

    # Make the API Call
    response = requests.request(action, api_url, params=params, headers=headers, data=json.dumps(data))

    # Check for an error to retry, re-auth, or fail
    if response.status_code in retry_statuses:
        try_count = try_count + 1
        if try_count <= max_retries:
            time.sleep(retry_wait_timer)
            return pc_call_api(action=action, api_url=api_url, pc_settings=pc_settings, data=data, params=params,
                               try_count=try_count, max_retries=max_retries, auth_count=auth_count, auth_retries=auth_retries)
        else:
            response.raise_for_status()
    elif response.status_code in auth_statuses and pc_settings['jwt'] is not None:
        auth_count = auth_count + 1
        if auth_count <= auth_retries:
            pc_settings = pc_jwt_get(pc_settings)
            return pc_call_api(action=action, api_url=api_url, pc_settings=pc_settings, data=data, params=params,
                               try_count=try_count, max_retries=max_retries, auth_count=auth_count,auth_retries=auth_retries)
        else:
            response.raise_for_status()
    else:
        response.raise_for_status()

    # Check for valid response and catch if blank or unexpected
    api_response_package = {}
    api_response_package['statusCode'] = response.status_code
    try:
        api_response_package['data'] = response.json()
    except ValueError:
        if response.text == '':
            api_response_package['data'] = None
        else:
            pc_lib_general.pc_exit_error(501, 'The server returned an unexpected server response.')
    return pc_settings, api_response_package


# Get JWT for access
def pc_jwt_get(pc_settings):
    url = "https://" + pc_settings['apiBase'] + "/login"
    action = "POST"
    pc_settings['jwt'] = pc_call_api(action, url, pc_settings, data=pc_settings)[1]['data']['token']
    return pc_settings


# Get Compliance Standards list
def api_compliance_standard_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/compliance"
    return pc_call_api(action, url, pc_settings)


# Add a new Compliance Standard
def api_compliance_standard_add(pc_settings, compliance_standard_new):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/compliance"
    return pc_call_api(action, url, pc_settings, data=compliance_standard_new)


# Get Compliance Standards Requirements list
def api_compliance_standard_requirement_list_get(pc_settings, compliance_standard_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_standard_id + "/requirement"
    return pc_call_api(action, url, pc_settings)


# Add a new Compliance Standard Requirement
def api_compliance_standard_requirement_add(pc_settings, compliance_standard_id, compliance_requirement_new):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_standard_id + "/requirement"
    return pc_call_api(action, url, pc_settings, data=compliance_requirement_new)


# Get Compliance Standards Requirements Sections list
def api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_requirement_id + "/section"
    return pc_call_api(action, url, pc_settings)


# Add a new Compliance Standard Requirement Section
def api_compliance_standard_requirement_section_add(pc_settings, compliance_requirement_id, compliance_section_new):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_requirement_id + "/section"
    return pc_call_api(action, url, pc_settings, data=compliance_section_new)


# Delete a Compliance Standard
def api_compliance_standard_delete(pc_settings, compliance_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/compliance/" + compliance_id
    return pc_call_api(action, url, pc_settings)


# Get Compliance Standards Policy list
def api_compliance_standard_policy_list_get(pc_settings, source_compliance_standard_name):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/policy"
    filters = [('policy.complianceStandard', source_compliance_standard_name)]
    return pc_call_api(action, url, pc_settings, params=filters)


# Get Compliance Standards Policy list (v2)
def api_compliance_standard_policy_v2_list_get(pc_settings, source_compliance_standard_name):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/policy"
    filters = [('policy.complianceStandard', source_compliance_standard_name)]
    return pc_call_api(action, url, pc_settings, params=filters)


# Get Policy list
def api_policy_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/policy"
    return pc_call_api(action, url, pc_settings)


# Get Policy list (v2)
def api_policy_v2_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/policy"
    return pc_call_api(action, url, pc_settings)


# Get Custom Policy list (v2)
def api_policy_custom_v2_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/policy"
    filters = [('policy.policyMode', 'custom')]
    return pc_call_api(action, url, pc_settings, params=filters)


# Get a Policy
def api_policy_get(pc_settings, policy_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/policy/" + policy_id
    return pc_call_api(action, url, pc_settings)


# Add a Policy
def api_policy_add(pc_settings, policy_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/policy"
    return pc_call_api(action, url, pc_settings, data=policy_to_add)


# Update a Policy
def api_policy_update(pc_settings, policy_id, policy_update):
    action = "PUT"
    url = "https://" + pc_settings['apiBase'] + "/policy/" + policy_id
    return pc_call_api(action, url, pc_settings, data=policy_update)


# Update Policy status
def api_policy_status_update(pc_settings, policy_id, status):
    action = "PATCH"
    url = "https://" + pc_settings['apiBase'] + "/policy/" + policy_id + "/status/" + status
    return pc_call_api(action, url, pc_settings)


# Delete a Policy
def api_policy_delete(pc_settings, policy_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/policy/" + policy_id
    return pc_call_api(action, url, pc_settings)


# Get Saved Search list
def api_saved_search_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/search/history?filter=saved"
    return pc_call_api(action, url, pc_settings)


# Get a Saved Search
def api_search_get(pc_settings, search_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/search/history/" + search_id
    return pc_call_api(action, url, pc_settings)


# Add a Saved Search
def api_saved_search_add(pc_settings, type_of_search, search_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/search/history/" + type_of_search
    return pc_call_api(action, url, pc_settings, data=search_to_add)


def api_search_add(pc_settings, type_of_search, search_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/search/" + type_of_search
    if type_of_search=='network':
        url="https://" + pc_settings['apiBase'] + "/search"
    return pc_call_api(action, url, pc_settings, data=search_to_add)


# Delete a Saved Search
def api_saved_search_delete(pc_settings, search_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/search/history/" + search_id
    return pc_call_api(action, url, pc_settings)


# Get User Role list
def api_user_role_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/user/role"
    return pc_call_api(action, url, pc_settings)


# Get User list
def api_user_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/user"
    return pc_call_api(action, url, pc_settings)


# Get a User
def api_user_get(pc_settings, useremail):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/user/" + useremail
    return pc_call_api(action, url, pc_settings)


# Add new User
def api_user_add(pc_settings, user_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/user"
    return pc_call_api(action, url, pc_settings, data=user_to_add)


# Update a User
def api_user_update(pc_settings, user_to_update):
    action = "PUT"
    url = "https://" + pc_settings['apiBase'] + "/user/" + user_to_update['email']
    return pc_call_api(action, url, pc_settings, data=user_to_update)


# Get Alerts list with filters
def api_alert_list_get(pc_settings, params=None, data=None):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/alert"
    return pc_call_api(action, url, pc_settings, params=params, data=data)


# Get Alerts list with filters (V2)
def api_alert_v2_list_get(pc_settings, params=None, data=None):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/v2/alert"
    return pc_call_api(action, url, pc_settings, params=params, data=data)


# Get Compliance Reports list
def api_compliance_report_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/report"
    return pc_call_api(action, url, pc_settings)


# Add Compliance Report
def api_compliance_report_add(pc_settings, report_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/report"
    return pc_call_api(action, url, pc_settings, data=report_to_add)


# Delete Compliance Report
def api_compliance_report_delete(pc_settings, report_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/report/" + report_id
    return pc_call_api(action, url, pc_settings)


# Download Compliance Report
def api_compliance_report_download(pc_settings, report_id):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/report/" + report_id + "/download"
    jwt, response_status, response_json = pc_call_api(action, url, pc_settings)
    if response_status == 204:
        #download pending
        pass
    elif response_status == 200:
        #download ready
        pass


# Get Cloud Accounts list
def api_cloud_accounts_list_get(pc_settings, params=None):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/cloud"
    return pc_call_api(action, url, pc_settings, params=params)


# Get Cloud Accounts Names list
def api_cloud_accounts_list_names_get(pc_settings, params=None):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/cloud/name"
    return pc_call_api(action, url, pc_settings, params=params)


# Add Cloud Account
def api_cloud_accounts_add(pc_settings, cloud_type, cloud_account_to_add):
    action = "POST"
    url = "https://" + pc_settings['apiBase'] + "/cloud/" + cloud_type
    return pc_call_api(action, url, pc_settings, data=cloud_account_to_add)


# Get Cloud Account Group list
def api_cloud_account_group_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/cloud/group"
    return pc_call_api(action, url, pc_settings)


# Delete Account Group
def api_cloud_account_group_delete(pc_settings, group_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/cloud/group/" + group_id
    return pc_call_api(action, url, pc_settings)


# Get Alert Rule list (V2)
def api_alert_rule_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/v2/alert/rule"
    return pc_call_api(action, url, pc_settings)


# Delete Alert Rule
def api_alert_rule_delete(pc_settings, rule_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/alert/rule/" + rule_id
    return pc_call_api(action, url, pc_settings)


# Get Integration list (V2)
def api_integration_list_get(pc_settings):
    action = "GET"
    url = "https://" + pc_settings['apiBase'] + "/integration"
    return pc_call_api(action, url, pc_settings)


# Delete Integration
def api_integration_delete(pc_settings, integration_id):
    action = "DELETE"
    url = "https://" + pc_settings['apiBase'] + "/integration/" + integration_id
    return pc_call_api(action, url, pc_settings)
