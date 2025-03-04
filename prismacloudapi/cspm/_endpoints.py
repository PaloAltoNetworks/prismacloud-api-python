""" Prisma Cloud API Endpoints Class """
import logging
import pprint


# TODO: Split into multiple files, one per endpoint ...

# pylint: disable=too-many-public-methods


class EndpointsPrismaCloudAPIMixin():
    """ Prisma Cloud API Endpoints Class """

    def current_user(self):
        return self.execute('GET', 'user/me')

    """
    Note: Eventually, all objects covered should have full CRUD capability, ie, to create, read, update, and delete (and list).

    Template

    [ ] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    """

    """
    Alerts

    [x] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    Additional:
    [x] LIST (v2)
    """

    def alert_list_read(self, query_params=None, body_params=None):
        # returns items directly
        return self.execute('POST', 'alert', query_params=query_params, body_params=body_params)

    def alert_v2_list_read(self, query_params=None, body_params=None):
        # returns items in results['items']. But really does not respect paginatin request.
        return self.execute_paginated('POST', 'v2/alert', query_params=query_params, body_params=body_params)

    def alert_csv_create(self, body_params=None):
        return self.execute('POST', 'alert/csv', body_params=body_params)

    def alert_csv_status(self, csv_report_id):
        return self.execute('GET', 'alert/csv/%s/status' % csv_report_id)

    def alert_csv_download(self, csv_report_id):
        return self.execute('GET', 'alert/csv/%s/download' % csv_report_id)

    """
    Policies

    [x] LIST
    [x] CREATE
    [x] READ
    [x] UPDATE
    [x] DELETE
    Additional:
    [x] LIST (v2)
    [x] LIST (v2) CUSTOM
    [x] UPDATE STATUS
    """

    def policy_list_read(self):
        return self.execute('GET', 'policy')

    def policy_v2_list_read(self):
        return self.execute('GET', 'v2/policy')

    def policy_custom_v2_list_read(self):
        filters = [('policy.policyMode', 'custom')]
        return self.execute('GET', 'v2/policy', query_params=filters)

    def policy_create(self, policy_to_add):
        return self.execute('POST', 'policy', body_params=policy_to_add)

    def policy_read(self, policy_id, message=None):
        self.progress(message)
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
    [x] CREATE
    [x] READ
    [ ] UPDATE
    [x] DELETE
    """

    def saved_search_list_read(self):
        return self.execute('GET', 'search/history?filter=saved')

    def saved_search_create(self, type_of_search, saved_search_to_add):
        if type_of_search == 'network':
            return self.execute('POST', 'search', body_params=saved_search_to_add)
        if type_of_search == 'audit_event':
            return self.execute('POST', 'search/event', body_params=saved_search_to_add)
        return self.execute('POST', 'search/%s' % type_of_search, body_params=saved_search_to_add)

    def saved_search_read(self, saved_search_id, message=None):
        self.progress(message)
        return self.execute('GET', 'search/history/%s' % saved_search_id)

    def saved_search_delete(self, saved_search_id):
        return self.execute('DELETE', 'search/history/%s' % saved_search_id)

    """
    Compliance Posture

    [x] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    """
    def compliance_posture_statistics(self):
        """Get Compliance Statistics Breakdown V2
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-compliance-posture-v-2/>`_
        """
        return self.execute('GET', 'v2/compliance/posture')

    def compliance_posture_statistics_post(self, body_params):
        """Get Compliance Statistics Breakdown V2"""
        return self.execute('POST', 'v2/compliance/posture', body_params=body_params)

    def compliance_posture_statistics_for_standard(self, compliance_id):
        """Get Compliance Statistics for Standard ID V2
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-compliance-posture-for-standard-v-2/>`_
        """
        return self.execute('GET', f'v2/compliance/posture/{compliance_id}')

    def compliance_posture_statistics_for_standard_post(self, compliance_id, body_params):
        """Get Compliance Statistics for Standard ID V2"""
        return self.execute('POST', f'v2/compliance/posture/{compliance_id}', body_params=body_params)

    def compliance_posture_statistics_for_requirement(self, compliance_id, requirement_id):
        """Get Compliance Statistics for Requirement ID V2
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-compliance-posture-for-requirement-v-2/>`_
        """
        return self.execute('GET', f'v2/compliance/posture/{compliance_id}/{requirement_id}')

    def compliance_posture_statistics_for_requirement_post(self, compliance_id, requirement_id, body_params):
        """Get Compliance Statistics for Requirement ID V2"""
        return self.execute('POST', f'v2/compliance/posture/{compliance_id}/{requirement_id}', body_params=body_params)

    def compliance_posture_trend(self):
        """Get Compliance Trend V2
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-compliance-posture-trend-for-standard-v-2/>`_
        """
        return self.execute('GET', 'v2/compliance/posture/trend')

    def compliance_posture_trend_post(self, body_params):
        """Get Compliance Trend V2"""
        return self.execute('POST', 'v2/compliance/posture/trend', body_params=body_params)

    def compliance_posture_trend_for_standard(self, compliance_id):
        """Get Compliance Trend for Standard ID V2
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-compliance-posture-trend-for-standard-v-2/>`_
        """
        return self.execute('GET', f'v2/compliance/posture/trend/{compliance_id}')

    def compliance_posture_trend_for_standard_post(self, compliance_id, body_params):
        """Get Compliance Trend for Standard ID V2"""
        return self.execute('POST', f'v2/compliance/posture/trend/{compliance_id}', body_params=body_params)

    def compliance_posture_trend_for_requirement(self, compliance_id, requirement_id):
        """Get Compliance Trend for Requirement ID V2
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-compliance-posture-trend-for-requirement-v-2/>`_
        """
        return self.execute('GET', f'v2/compliance/posture/trend/{compliance_id}/{requirement_id}')

    def compliance_posture_trend_for_requirement_post(self, compliance_id, requirement_id, body_params):
        """Get Compliance Trend for Requirement ID V2 """
        return self.execute('POST', f'v2/compliance/posture/trend/{compliance_id}/{requirement_id}', body_params=body_params)


    """
    Compliance Standards

    [x] LIST
    [x] CREATE
    [x] READ
    [ ] UPDATE
    [x] DELETE
    """

    def compliance_standard_list_read(self):
        return self.execute('GET', 'compliance')

    def compliance_standard_create(self, compliance_standard_to_add):
        return self.execute('POST', 'compliance', body_params=compliance_standard_to_add)

    def compliance_standard_read(self, compliance_standard_id):
        return self.execute('GET', 'compliance/%s' % compliance_standard_id)

    def compliance_standard_delete(self, compliance_standard_id):
        return self.execute('DELETE', 'compliance/%s' % compliance_standard_id)

    """
    Compliance Standard Requirements

    [x] LIST
    [x] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    """

    def compliance_standard_requirement_list_read(self, compliance_standard_id):
        return self.execute('GET', 'compliance/%s/requirement' % compliance_standard_id)

    def compliance_standard_requirement_create(self, compliance_standard_id, compliance_requirement_to_add):
        return self.execute('POST', 'compliance/%s/requirement' % compliance_standard_id,
                            body_params=compliance_requirement_to_add)

    """
    Compliance Standard Requirements Sections

    [x] LIST
    [x] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    """

    def compliance_standard_requirement_section_list_read(self, compliance_requirement_id):
        return self.execute('GET', 'compliance/%s/section' % compliance_requirement_id)

    def compliance_standard_requirement_section_create(self, compliance_requirement_id, compliance_section_to_add):
        return self.execute('POST', 'compliance/%s/section' % compliance_requirement_id,
                            body_params=compliance_section_to_add)

    """
    Compliance Standard Requirements Policies

    [x] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    Additional:
    [x] LIST (v2)

    """

    def compliance_standard_policy_list_read(self, compliance_standard_name):
        filters = [('policy.complianceStandard', compliance_standard_name)]
        return self.execute('GET', 'policy', query_params=filters)

    def compliance_standard_policy_v2_list_read(self, compliance_standard_name):
        filters = [('policy.complianceStandard', compliance_standard_name)]
        return self.execute('GET', 'v2/policy', query_params=filters)

    """
    Users

    [x] LIST
    [x] CREATE
    [x] READ
    [x] UPDATE
    [x] DELETE
    """

    def user_list_read_v3(self):
        return self.execute('GET', 'v3/user')

    def user_list_read_v2(self):
        return self.execute('GET', 'v2/user')

    def user_create(self, user):
        return self.execute('POST', 'v2/user', body_params=user)

    def user_read(self, user_id):
        return self.execute('GET', 'v2/user/%s' % user_id)

    def user_update(self, user):
        return self.execute('PUT', 'v2/user/%s' % user['email'], body_params=user)

    def user_delete(self, user_id):
        return self.execute('DELETE', 'user/%s' % user_id)

    def user_list_user_emails(self):
        return self.execute('GET', 'user/name')

    def user_list_email_domains(self):
        return self.execute('GET', 'user/domain')

    def user_list_bypass_sso(self):
        return self.execute('GET', 'user/saml/bypass')

    def user_update_bypass_sso(self, body_params):
        return self.execute('PUT', 'user/saml/bypass', body_params=body_params)

    """
    User Roles

    [x] LIST
    [ ] CREATE
    [x] READ
    [x] UPDATE
    [x] DELETE
    """

    def user_role_list_read(self):
        return self.execute('GET', 'user/role')

    def user_role_create(self, user_role_to_add):
        return self.execute('POST', 'user/role', body_params=user_role_to_add)

    def user_role_update(self, user_role_id, user_role_update):
        return self.execute('PUT', 'user/role/%s' % user_role_id, body_params=user_role_update)

    def user_role_read(self, user_role_id):
        return self.execute('GET', 'user/role/%s' % user_role_id)

    def user_role_delete(self, user_role_id):
        return self.execute('DELETE', 'user/role/%s' % user_role_id)

    """
    Access Keys

    [x] LIST
    [x] CREATE
    [x] READ
    [x] UPDATE
    [x] DELETE
    Additional:
    [x] UPDATE STATUS
    """

    def access_keys_list_read(self):
        return self.execute('GET', 'access_keys')

    def access_key_create(self, access_key_to_add):
        return self.execute('POST', 'access_keys', body_params=access_key_to_add)

    def access_key_read(self, access_key_id):
        return self.execute('GET', 'access_keys/%s' % access_key_id)

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
    [x] CREATE
    [ ] READ
    [x] UPDATE
    [x] DELETE
    Additional:
    [x] LIST NAMES
    """

    def cloud_accounts_list_read(self, query_params=None):
        return self.execute('GET', 'cloud', query_params=query_params)

    def cloud_accounts_children_list_read(self, cloud_account_type, cloud_account_id):
        return self.execute('GET', 'cloud/%s/%s/project' % (cloud_account_type, cloud_account_id))

    def cloud_accounts_list_names_read(self, query_params=None):
        return self.execute('GET', 'cloud/name', query_params=query_params)

    def cloud_accounts_create(self, cloud_type, cloud_account_to_add):
        return self.execute('POST', 'cloud/%s' % cloud_type, body_params=cloud_account_to_add)

    def cloud_account_info_read(self, cloud_type, cloud_account_id):
        return self.execute('GET', 'cloud/%s/%s' % (cloud_type, cloud_account_id))

    def cloud_account_update(self, cloud_type, cloud_account_id, cloud_account_update):
        return self.execute('PUT', 'cloud/%s/%s' % (cloud_type, cloud_account_id), body_params=cloud_account_update)

    def cloud_account_delete(self, cloud_type, cloud_account_id):
        return self.execute('DELETE', 'cloud/%s/%s' % (cloud_type, cloud_account_id))

    def cloud_types_list_read(self, query_params=None):
        return self.execute('GET', 'cloud/type', query_params=query_params)

    """
    Cloud Account Groups

    [x] LIST
    [x] CREATE
    [x] READ
    [x] UPDATE
    [x] DELETE
    """

    def cloud_account_group_list_read(self):
        return self.execute('GET', 'cloud/group')

    def cloud_account_group_create(self, cloud_account_group_to_add):
        return self.execute('POST', 'cloud/group', body_params=cloud_account_group_to_add)

    def cloud_account_group_read(self, cloud_account_group_id):
        return self.execute('GET', 'cloud/group/%s' % cloud_account_group_id)

    def cloud_account_group_update(self, cloud_account_group_id, cloud_account_group_update):
        return self.execute('PUT', 'cloud/group/%s' % cloud_account_group_id, body_params=cloud_account_group_update)

    def cloud_account_group_delete(self, cloud_account_group_id):
        return self.execute('DELETE', 'cloud/group/%s' % cloud_account_group_id)

    """
    Asset (Resources) Inventory

    [x] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    Additional:
    [x] LIST (v2)
    [x] LIST WITH FILTERS(v2)
    """

    def asset_inventory_list_read(self, query_params=None):
        return self.execute('GET', 'v2/inventory', query_params=query_params)

    def asset_inventory_list_read_post(self, body_params=None):
        return self.execute('POST', 'v2/inventory', body_params=body_params)

    """
    Asset (Resources) Inventory V3

    [x] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    Additional:
    [x] LIST (v3)
    [x] LIST WITH FILTERS(v3)
    """

    def asset_inventory_list_read_v3(self, query_params=None):
        return self.execute('GET', 'v3/inventory', query_params=query_params)

    def asset_inventory_list_read_postv_3(self, body_params=None):
        return self.execute('POST', 'v3/inventory', body_params=body_params)

    """
    (Assets) Resources

    [ ] LIST
    [ ] CREATE
    [x] READ
    [ ] UPDATE
    [ ] DELETE
    """

    def resource_read(self, body_params=None, force=False, message=None):
        self.progress(message)
        return self.execute('POST', 'resource', body_params=body_params, force=force)

    def resource_network_read(self, body_params=None, force=False):
        return self.execute('POST', 'resource/network', body_params=body_params, force=force)

    def resource_scan_info_read(self, body_params=None):
        result = []
        page_number = 1
        while page_number == 1 or 'pageToken' in body_params:
            api_response = self.execute(
                'POST', 'resource/scan_info', body_params=body_params)
            if 'resources' in api_response:
                result.extend(api_response['resources'])
            if 'nextPageToken' in api_response:
                body_params['pageToken'] = api_response['nextPageToken']
            else:
                body_params.pop('pageToken', None)
            # if 'totalMatchedCount' in api_response:
            #    self.progress('Resources: %s, Page Size: %s, Page: %s' % (api_response['totalMatchedCount'], body_params['limit'], page_number))
            page_number += 1
        return result

    """
    Alert Rules

    [x] LIST
    [x] CREATE
    [x] READ
    [x] UPDATE
    [x] DELETE
    Additional:
    [x] LIST (v2)
    """

    def alert_rule_list_read(self):
        return self.execute('GET', 'v2/alert/rule')

    def alert_rule_create(self, alert_rule):
        return self.execute('POST', 'alert/rule', body_params=alert_rule)

    def alert_rule_read(self, alert_rule_id):
        return self.execute('GET', 'alert/rule/%s' % alert_rule_id)

    def alert_rule_delete(self, alert_rule_id):
        return self.execute('DELETE', 'alert/rule/%s' % alert_rule_id)

    def alert_rule_update(self, alert_rule_id, alert_rule_update):
        return self.execute('PUT', 'alert/rule/%s' % alert_rule_id, body_params=alert_rule_update)

    """
    Integrations

    [x] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [x] DELETE
    Additional:
    [ ] LIST (v2)
    """

    def integration_list_read(self):
        return self.execute('GET', 'integration')

    def integration_delete(self, integration_id):
        return self.execute('DELETE', 'integration/%s' % integration_id)

    def integration_list(self, tenant_id):
        # use
        return self.execute('GET', f'v1/tenant/{tenant_id}/integration')


    """
    Resource Lists

    [x] LIST
    [X] CREATE
    [ ] READ
    [ ] UPDATE
    [x] DELETE
    """

    def resource_list_read(self):
        return self.execute('GET', 'v1/resource_list')

    def resource_list_delete(self, resource_list_id):
        return self.execute('DELETE', 'v1/resource_list/%s' % resource_list_id)

    def resource_list_create(self, resource_list_to_add):
        return self.execute('POST', 'v1/resource_list', body_params=resource_list_to_add)

    """
    Adoption Advisor

    [x] LIST
    [X] CREATE
    [ ] READ
    [X] UPDATE
    [X] DELETE
    """

    def adoptionadvisor_report_read(self):
        return self.execute('GET', 'adoptionadvisor/report')

    def adoptionadvisor_report_delete(self, report_id):
        return self.execute('DELETE', 'adoptionadvisor/report/%s' % report_id)

    def adoptionadvisor_report_create(self, report_to_add):
        return self.execute('POST', 'adoptionadvisor/report', body_params=report_to_add)

    """
    Compliance Reports

    [x] LIST
    [x] CREATE
    [ ] READ
    [ ] UPDATE
    [x] DELETE
    Additional:
    [x] DOWNLOAD
    """

    def compliance_report_list_read(self):
        return self.execute('GET', 'report')

    def compliance_report_create(self, report_to_add):
        return self.execute('POST', 'report', body_params=report_to_add)

    def compliance_report_delete(self, report_id):
        return self.execute('DELETE', 'report/%s' % report_id)

    def compliance_report_download(self, report_id):
        """
        Download Report
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/download-report/>`_
        """
        return self.execute('GET', f'report/{report_id}/download')

    def compliance_report_history(self, report_id):
        return self.execute('GET', f'report/{report_id}/history')

    def compliance_report_type_list(self):
        """
        Get Report Types
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-report-types/>`_
        """
        return self.execute('GET', 'report/type')

    def compliance_report_type_get(self, report_id):
        """
        Get Report Config
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-specified-report/>`_
        """
        return self.execute('GET', f'report/type/{report_id}')


    """
    Search

    [ ] LIST
    [ ] CREATE
    [x] READ
    [ ] UPDATE
    [ ] DELETE
    """

    def search_config_read(self, query, search_id=None, search_name=None, search_description=None, limit=100,
                           with_resource_json=None, time_range=None, sort=None, heuristic_search=None,
                           paginate=True):
        """
        Perform Config Search
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/search-config/>`_
        """
        # if time_range is None:
        #     time_range = dict(type="relative", value=dict(unit="hour", amount=24))
        body_params = dict(query=query, id=search_id, searchName=search_name, searchDescription=search_description,
                           limit=limit, withResourceJson=with_resource_json, timeRange=time_range, sort=sort,
                           heuristicSearch=heuristic_search)
        for k, v in dict(body_params).items():
            if v is None:
                del body_params[k]
        next_page_token = None
        # https://pan.dev/prisma-cloud/api/cspm/search-config/
        api_response = self.execute('POST', 'search/config', body_params=body_params)
        # logging.debug(pprint.pformat(api_response))
        if 'data' in api_response and 'items' in api_response['data']:
            yield from api_response['data']['items']
            next_page_token = api_response['data'].pop('nextPageToken', None)
        while paginate and next_page_token:
            body_params['pageToken'] = next_page_token
            # https://pan.dev/prisma-cloud/api/cspm/search-config-page/
            # logging.debug("paging %s", pprint.pformat(body_params))
            api_response = self.execute('POST', 'search/config/page', body_params=body_params)
            # logging.debug(pprint.pformat(api_response))
            if 'items' in api_response:
                yield from api_response['items']
            next_page_token = api_response.pop('nextPageToken', None)
        return

    def search_config_read_by_query(self, query, skip_search_creation=None, skip_results=None, limit=100,
                                    with_resource_json=None, time_range=None,
                                    sort=None, next_page_token=None, paginate=True):
        """
        Perform Config Search by Query
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/search-config-by-query/>`_
        """
        # if time_range is None:
        #     time_range = dict(type="relative", value=dict(unit="hour", amount=24))
        body_params = dict(query=query, skipSearchCreation=skip_search_creation, limit=limit,
                           withResourceJson=with_resource_json, timeRange=time_range,
                           skipResult=skip_results,
                           sort=sort,
                           nextPageToken=next_page_token)
        for k, v in dict(body_params).items():
            if v is None:
                del body_params[k]
        next_page_token = None
        api_response = self.execute('POST', f'search/api/v1/config', body_params=body_params)
        if 'items' in api_response:
            yield from api_response['items']
            next_page_token = api_response.pop('nextPageToken', None)
        while paginate and next_page_token:
            body_params['nextPageToken'] = next_page_token
            api_response = self.execute('POST', f'search/api/v1/config', body_params=body_params)
            if 'items' in api_response:
                yield from api_response['items']
            next_page_token = api_response.pop('nextPageToken', None)
        return

    def search_config_read_by_search_id(self, search_id, limit=100, with_resource_json=None, time_range=None,
                                        sort=None, next_page_token=None, paginate=True):
        """
        Perform Config Search by Search Id
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/search-config-by-search-id/>`_
        """
        # if time_range is None:
        #     time_range = dict(type="relative", value=dict(unit="hour", amount=24))
        body_params = dict(limit=limit, withResourceJson=with_resource_json, timeRange=time_range, sort=sort,
                           nextPageToken=next_page_token)
        for k, v in dict(body_params).items():
            if v is None:
                del body_params[k]
        next_page_token = None
        api_response = self.execute('POST', f'search/api/v1/config/{search_id}', body_params=body_params)
        if 'items' in api_response:
            yield from api_response['items']
            next_page_token = api_response.pop('nextPageToken', None)
        while paginate and next_page_token:
            body_params['nextPageToken'] = next_page_token
            api_response = self.execute('POST', f'search/api/v1/config/{search_id}', body_params=body_params)
            if 'items' in api_response:
                yield from api_response['items']
            next_page_token = api_response.pop('nextPageToken', None)
        return

    def search_config_read_v2(self, query, start_time=None, skip_results=None, limit=100,
                                    with_resource_json=None, # time_range=None,
                                    sort=None, next_page_token=None, paginate=True):
        """
        Perform Config Search V2
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/search-config-v-2/>`_
        """
        # if time_range is None:
        #     time_range = dict(type="relative", value=dict(unit="hour", amount=24))
        body_params = dict(query=query, limit=limit, startTime=start_time,
                           withResourceJson=with_resource_json, # timeRange=time_range,
                           skipResult=skip_results,
                           sort=sort,
                           nextPageToken=next_page_token)
        for k, v in dict(body_params).items():
            if v is None:
                del body_params[k]
        next_page_token = None
        api_response = self.execute('POST', f'search/api/v2/config', body_params=body_params)
        if 'items' in api_response:
            yield from api_response['items']
            next_page_token = api_response.pop('nextPageToken', None)
        while paginate and next_page_token:
            body_params['nextPageToken'] = next_page_token
            api_response = self.execute('POST', f'search/api/v2/config', body_params=body_params)
            if 'items' in api_response:
                yield from api_response['items']
            next_page_token = api_response.pop('nextPageToken', None)
        return


    def search_network_read(self, search_params, filtered=False):
        search_url = 'search'
        if filtered:
            search_url = 'search/filtered'
        return self.execute('POST', search_url, body_params=search_params)

    def search_event_read(self, search_params, subsearch=None):
        result = []
        next_page_token = None
        search_url = 'search/event'
        if subsearch and subsearch in ['aggregate', 'filtered']:
            search_url = 'search/event/%s' % subsearch
        api_response = self.execute_paginated(
            'POST', search_url, body_params=search_params)
        if 'data' in api_response and 'items' in api_response['data']:
            result = api_response['data']['items']
            next_page_token = api_response['data'].pop('nextPageToken', None)
        while next_page_token:
            api_response = self.execute_paginated(
                'POST', 'search/config/page', body_params={'limit': 1000, 'pageToken': next_page_token})
            if 'items' in api_response:
                result.extend(api_response['items'])
            next_page_token = api_response.pop('nextPageToken', None)
        return result

    def search_iam_read(self, search_params):
        result = []
        next_page_token = None
        api_response = self.execute_paginated(
            'POST', 'api/v1/permission', body_params=search_params)
        if 'data' in api_response and 'items' in api_response['data']:
            result = api_response['data']['items']
            next_page_token = api_response['data'].pop('nextPageToken', None)
        while next_page_token:
            api_response = self.execute_paginated(
                'POST', 'api/v1/permission/page',
                body_params={'limit': 1000, 'pageToken': next_page_token, 'withResourceJson': 'true'})
            if 'items' in api_response:
                result.extend(api_response['items'])
            next_page_token = api_response.pop('nextPageToken', None)
        return result

    def search_iam_source_to_granter(self, search_params):
        search_url = 'api/v1/permission/graph/source_to_granter'
        return self.execute('POST', search_url, body_params=search_params)

    def search_iam_granter_to_dest(self, search_params):
        search_url = 'api/v1/permission/graph/granter_to_dest'
        return self.execute('POST', search_url, body_params=search_params)

    def search_suggest_list_read(self, query_to_suggest):
        return self.execute('POST', 'search/suggest', body_params=query_to_suggest)

    """
    Configuration

    [ ] LIST
    [ ] CREATE
    [x] READ
    [ ] UPDATE
    [ ] DELETE
    """

    def compute_config(self):
        return self.execute('GET', 'compute/config')

    def meta_info(self):
        return self.execute('GET', 'meta_info')

    """
    Usage

    [ ] LIST
    [ ] CREATE
    [x] READ
    [ ] UPDATE
    [ ] DELETE
    """

    def resource_usage_by_cloud_type(self, body_params):
        return self.execute('POST', 'license/api/v1/usage', body_params=body_params)

    def resource_usage_over_time(self, body_params):
        return self.execute('POST', 'license/api/v1/usage/time_series', body_params=body_params)

    def resource_usage_by_cloud_type_v2(self, body_params):
        return self.execute('POST', 'license/api/v2/usage', body_params=body_params)

    def resource_usage_over_time_v2(self, body_params):
        return self.execute('POST', 'license/api/v2/time_series', body_params=body_params)

    """
    SSO SAML

    [X] LIST
    [X] CREATE
    [X] READ
    [X] UPDATE
    [ ] DELETE
    """

    def saml_config_read(self):
        return self.execute('GET', 'authn/v1/saml/config')

    def saml_config_create(self, body_params):
        return self.execute('POST', 'authn/v1/saml/config', body_params=body_params)

    def saml_config_update(self, body_params):
        return self.execute('PUT', 'authn/v1/saml/config', body_params=body_params)

    def oidc_config_read(self):
        """
        Get OIDC Configuration
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-oauth-2-config/>`_
        """
        return self.execute('GET', 'authn/v1/oauth2/config')

    """
    Permission groups 
    """
    def permission_group_list(self):
        """
        Get All Permission Groups
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-all/>`_
        """
        return self.execute('GET', 'authz/v1/permission_group')

    def permission_group_get(self, group_id, include_associated_roles: bool=None):
        """
        Get Permission Group by ID
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-1/>`_
        """
        query_params = dict()
        if include_associated_roles:
            query_params=dict(includeAssociatedRoles=include_associated_roles)
        return self.execute('GET', f'authz/v1/permission_group/{group_id}', query_params=query_params)

    def permission_group_feature_list(self):
        """
        Get All Active Features
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-features/>`_
        """
        return self.execute('GET', 'authz/v1/feature')


    """
    Enterprise Settings 

    [ ] LIST
    [ ] CREATE
    [X] READ
    [X] UPDATE
    [ ] DELETE
    """

    def enterprise_settings_config(self, body_params):
        return self.execute('POST', 'settings/enterprise', body_params=body_params)

    def enterprise_settings(self):
        return self.execute('GET', 'settings/enterprise')

    """
    Anomaly Settings 

    [ ] LIST
    [ ] CREATE
    [ ] READ
    [X] UPDATE
    [ ] DELETE
    """

    def anomaly_settings_config(self, body_params, policy_id):
        anomaly_url = 'anomalies/settings/%s' % policy_id
        return self.execute('POST', anomaly_url, body_params=body_params)

    """
    Check the other side

    [ ] LIST
    [ ] CREATE
    [X] READ
    [X] UPDATE
    [ ] DELETE
    """

    def check(self):
        return self.execute('GET', 'check')

    """
    Background jobs, Reports
    """
    def report_metadata(self, query_params=None):
        """
        This endpoint is available on the Prisma Cloud Darwin release only.

        Get Reports Metadata
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/list-reports/>`_
        """
        return self.execute('GET', 'report-service/api/v1/report', query_params=query_params)



    """
    Notifications Templates
    """
    def templates_list(self):
        """
        List Templates
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-all-templates-v-1/>`_
        """
        return self.execute('GET', f'api/v1/tenant/{self.tenant_id}/template')

    def templates_get(self, template_id):
        """
        Get Template
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-template-v-1/>`_
        """
        return self.execute('GET', f'api/v1/tenant/{self.tenant_id}/template/{template_id}')

    """
    Cloud Ingested Logs
    """
    def aws_eventbridge_configuration_for_account(self, tenant_id, account_id):
        """
        Get AWS Eventbridge configuration details
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-eventbridge-configuration-details/>`_
        """
        return self.execute('GET', f'audit_logs/v2/tenant/{tenant_id}/aws_accounts/{account_id}/eventbridge_config')

    def aws_eventbridge_configuration_for_account(self, account_id):
        """
        Fetch AWS S3 Flow Log details
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cspm/get-aws-s-3-flowlog/>`_
        """
        return self.execute('GET', f'cloud-accounts-manager/v1/cloud-accounts/aws/{account_id}/features/aws-flow-logs/s3')
