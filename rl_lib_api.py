import json
import requests
import time
import rl_lib_general

# --Description-- #
# Redlock API Helper library.  Contains shared API call functions.
# --End Description-- #


# --Helper Methods-- #
# Main API Call Function
def rl_call_api(action, api_url, rl_settings, data=None, params=None, try_count=1, max_retries=3, auth_count=0, auth_retries=1):
    retry_statuses = [429, 500, 502, 503, 504]
    auth_statuses = [401]
    retry_wait_timer = 5
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': rl_settings['jwt']}

    # Make the API Call
    response = requests.request(action, api_url, params=params, headers=headers, data=json.dumps(data))

    # Check for an error to retry, re-auth, or fail
    if response.status_code in retry_statuses:
        try_count = try_count + 1
        if try_count <= max_retries:
            time.sleep(retry_wait_timer)
            return rl_call_api(action=action, api_url=api_url, rl_settings=rl_settings, data=data, params=params,
                               try_count=try_count, max_retries=max_retries, auth_count=auth_count,auth_retries=auth_retries)
        else:
            response.raise_for_status()
    elif response.status_code in auth_statuses and rl_settings['jwt'] is not None:
        auth_count = auth_count + 1
        if auth_count <= auth_retries:
            jwt = rl_jwt_get(rl_settings)
            return rl_call_api(action=action, api_url=api_url, rl_settings=rl_settings, data=data, params=params,
                               try_count=try_count, max_retries=max_retries, auth_count=auth_count,auth_retries=auth_retries)
        else:
            response.raise_for_status()
    else:
        response.raise_for_status()

    # Check for valid response and catch if blank or unexpected
    response_package = {}
    response_package['statusCode'] = response.status_code
    try:
        response_package['data'] = response.json()
    except ValueError:
        if response.text == '':
            response_package['data'] = None
        else:
            rl_lib_general.rl_exit_error(501, 'The server returned an unexpected server response.')
    return rl_settings, response_package


# Get JWT for access
def rl_jwt_get(rl_settings):
    url = "https://" + rl_settings['apiBase'] + "/login"
    action = "POST"
    rl_settings, response_package = rl_call_api(action, url, rl_settings, data=rl_settings)
    rl_settings['jwt'] = response_package['data']['token']
    return rl_settings, response_package


# Get Compliance Standards list
def api_compliance_standard_list_get(rl_settings):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/compliance"
    return rl_call_api(action, url, rl_settings)


# Add a new Compliance Standard
def api_compliance_standard_add(rl_settings, compliance_standard_new):
    action = "POST"
    url = "https://" + rl_settings['apiBase'] + "/compliance"
    return rl_call_api(action, url, rl_settings, data=compliance_standard_new)


# Get Compliance Standards Requirements list
def api_compliance_standard_requirement_list_get(rl_settings, compliance_standard_id):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/compliance/" + compliance_standard_id + "/requirement"
    return rl_call_api(action, url, rl_settings)


# Add a new Compliance Standard Requirement
def api_compliance_standard_requirement_add(rl_settings, compliance_standard_id, compliance_requirement_new):
    action = "POST"
    url = "https://" + rl_settings['apiBase'] + "/compliance/" + compliance_standard_id + "/requirement"
    return rl_call_api(action, url, rl_settings, data=compliance_requirement_new)


# Get Compliance Standards Requirements Sections list
def api_compliance_standard_requirement_section_list_get(rl_settings, compliance_requirement_id):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/compliance/" + compliance_requirement_id + "/section"
    return rl_call_api(action, url, rl_settings)


# Add a new Compliance Standard Requirement Section
def api_compliance_standard_requirement_section_add(rl_settings, compliance_requirement_id, compliance_section_new):
    action = "POST"
    url = "https://" + rl_settings['apiBase'] + "/compliance/" + compliance_requirement_id + "/section"
    return rl_call_api(action, url, rl_settings, data=compliance_section_new)


# Get Compliance Standards Policy list
def api_compliance_standard_policy_list_get(rl_settings, source_compliance_standard_name):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/policy"
    filters = [('policy.complianceStandard', source_compliance_standard_name)]
    return rl_call_api(action, url, rl_settings, params=filters)


# Get policy list
def api_policy_list_get(rl_settings):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/policy"
    return rl_call_api(action, url, rl_settings)


# Get a policy
def api_policy_get(rl_settings, policy_id):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/policy/" + policy_id
    return rl_call_api(action, url, rl_settings)


# Update a policy
def api_policy_update(rl_settings, policy_id, policy_update):
    action = "PUT"
    url = "https://" + rl_settings['apiBase'] + "/policy/" + policy_id
    return rl_call_api(action, url, rl_settings, data=policy_update)


# Update policy status
def api_policy_status_update(rl_settings, policy_id, status):
    action = "PATCH"
    url = "https://" + rl_settings['apiBase'] + "/policy/" + policy_id + "/status/" + status
    return rl_call_api(action, url, rl_settings)


# Get User Role list
def api_user_role_list_get(rl_settings):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/user/role"
    return rl_call_api(action, url, rl_settings)


# Get User list
def api_user_list_get(rl_settings):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/user"
    return rl_call_api(action, url, rl_settings)


# Get a User
def api_user_get(rl_settings, useremail):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/user/" + useremail
    return rl_call_api(action, url, rl_settings)


# Add new User
def api_user_add(rl_settings, user_to_add):
    action = "POST"
    url = "https://" + rl_settings['apiBase'] + "/user"
    return rl_call_api(action, url, rl_settings, data=user_to_add)


# Update a User
def api_user_update(rl_settings, user_to_update):
    action = "PUT"
    url = "https://" + rl_settings['apiBase'] + "/user/" + user_to_update['email']
    return rl_call_api(action, url, rl_settings, data=user_to_update)


# Get alert list with filters - DOES NOT WORK
def api_alert_list_get(rl_settings, params=None, data=None):
    action = "POST"
    url = "https://" + rl_settings['apiBase'] + "/alert"
    return rl_call_api(action, url, rl_settings, params=params, data=data, max_retries=0)


# Get Compliance Reports list
def api_compliance_report_list_get(rl_settings):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/report"
    return rl_call_api(action, url, rl_settings)


# Add Compliance Report
def api_compliance_report_add(rl_settings, report_to_add):
    action = "POST"
    url = "https://" + rl_settings['apiBase'] + "/report"
    return rl_call_api(action, url, rl_settings, data=report_to_add)


# Delete Compliance Reports
def api_compliance_report_delete(rl_settings, report_id):
    action = "DELETE"
    url = "https://" + rl_settings['apiBase'] + "/report/" + report_id
    return rl_call_api(action, url, rl_settings)


# Download Compliance Report
def api_compliance_report_download(rl_settings, report_id):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/report/" + report_id + "/download"
    jwt, response_status, response_json = rl_call_api(action, url, rl_settings)
    if response_status == 204:
        #download pending
        pass
    elif response_status == 200:
        #download ready
        pass


# Get Cloud Accounts list
def api_cloud_accounts_list_get(rl_settings):
    action = "GET"
    url = "https://" + rl_settings['apiBase'] + "/cloud"
    return rl_call_api(action, url, rl_settings)
