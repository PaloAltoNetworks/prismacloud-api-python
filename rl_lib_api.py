import json
import requests
import rl_lib_general

# --Description-- #
# Redlock API Helper library.  Contains shared API call functions.
# --End Description-- #


# --Helper Methods-- #
# Main API Call Function
def rl_call_api(action, api_url, jwt=None, data=None, params=None, count=0):
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': jwt}
    response = requests.request(action, api_url, params=params, headers=headers, data=json.dumps(data))
    # Check for successful API call
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        if response.text == '':
            return None
        else:
            rl_lib_general.rl_exit_error(501, 'The server returned an unexpected server response.')


# Get JWT for access (Needs data from rl_login_get)
def rl_jwt_get(rl_settings):
    url = "https://" + rl_settings['apiBase'] + "/login"
    action = "POST"
    response = rl_call_api(action, url, data=rl_settings)
    return response['token']


# Get Compliance Standards list
def api_compliance_standard_list_get(jwt, api_base):
    action = "GET"
    url = "https://" + api_base + "/compliance"
    return rl_call_api(action, url, jwt=jwt)


# Add a new Compliance Standard
def api_compliance_standard_add(jwt, api_base, compliance_standard_new):
    action = "POST"
    url = "https://" + api_base + "/compliance"
    return rl_call_api(action, url, jwt=jwt, data=compliance_standard_new)


# Get Compliance Standards Requirements list
def api_compliance_standard_requirement_list_get(jwt, api_base, compliance_standard_id):
    action = "GET"
    url = "https://" + api_base + "/compliance/" + compliance_standard_id + "/requirement"
    return rl_call_api(action, url, jwt=jwt)


# Add a new Compliance Standard Requirement
def api_compliance_standard_requirement_add(jwt, api_base, compliance_standard_id, compliance_requirement_new):
    action = "POST"
    url = "https://" + api_base + "/compliance/" + compliance_standard_id + "/requirement"
    return rl_call_api(action, url, jwt=jwt, data=compliance_requirement_new)


# Get Compliance Standards Requirements Sections list
def api_compliance_standard_requirement_section_list_get(jwt, api_base, compliance_requirement_id):
    action = "GET"
    url = "https://" + api_base + "/compliance/" + compliance_requirement_id + "/section"
    return rl_call_api(action, url, jwt=jwt)


# Add a new Compliance Standard Requirement Section
def api_compliance_standard_requirement_section_add(jwt, api_base, compliance_requirement_id, compliance_section_new):
    action = "POST"
    url = "https://" + api_base + "/compliance/" + compliance_requirement_id + "/section"
    return rl_call_api(action, url, jwt=jwt, data=compliance_section_new)


# Get Compliance Standards Policy list
def api_compliance_standard_policy_list_get(jwt, api_base, source_compliance_standard_name):
    action = "GET"
    url = "https://" + api_base + "/policy"
    filters = [('policy.complianceStandard', source_compliance_standard_name)]
    return rl_call_api(action, url, jwt=jwt, params=filters)


# Get policy list
def api_policy_list_get(jwt, api_base):
    action = "GET"
    url = "https://" + api_base + "/policy"
    return rl_call_api(action, url, jwt=jwt)


# Get a policy
def api_policy_get(jwt, api_base, policy_id):
    action = "GET"
    url = "https://" + api_base + "/policy/" + policy_id
    return rl_call_api(action, url, jwt=jwt)


# Update a policy
def api_policy_update(jwt, api_base, policy_id, policy_update):
    action = "PUT"
    url = "https://" + api_base + "/policy/" + policy_id
    return rl_call_api(action, url, jwt=jwt, data=policy_update)


# Update policy status
def api_policy_status_update(jwt, api_base, policy_id, status):
    action = "PATCH"
    url = "https://" + api_base + "/policy/" + policy_id + "/status/" + status
    return rl_call_api(action, url, jwt=jwt)


# Get User Role list
def api_user_role_list_get(jwt, api_base):
    action = "GET"
    url = "https://" + api_base + "/user/role"
    return rl_call_api(action, url, jwt=jwt)


# Get User list
def api_user_list_get(jwt, api_base):
    action = "GET"
    url = "https://" + api_base + "/user"
    return rl_call_api(action, url, jwt=jwt)


# Get a User
def api_user_get(jwt, api_base, useremail):
    action = "GET"
    url = "https://" + api_base + "/user/" + useremail
    return rl_call_api(action, url, jwt=jwt)


# Add new User
def api_user_add(jwt, api_base, user_to_add):
    action = "POST"
    url = "https://" + api_base + "/user"
    return rl_call_api(action, url, jwt=jwt, data=user_to_add)


# Update a User
def api_user_update(jwt, api_base, user_to_update):
    action = "PUT"
    url = "https://" + api_base + "/user/" + user_to_update['email']
    return rl_call_api(action, url, jwt=jwt, data=user_to_update)

