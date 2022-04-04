""" Requests and Output """

import json
import sys
import time

import requests

class PrismaCloudAPICodeSecurityMixin():
    """ Requests and Output """

    # pylint: disable=too-many-arguments,too-many-branches,too-many-locals,too-many-statements
    def execute_code_security(self, action, endpoint, query_params=None, body_params=None, force=False, paginated=False):
        self.suppress_warnings_when_ca_bundle_false()
        if not self.token:
            self.login()
        if int(time.time() - self.token_timer) > self.token_limit:
            self.extend_login()
        # Endpoints that return large numbers of results use a 'hasNext' key.
        # Pagination is via query parameters for both GET and POST, and appears to be specific to "List File Errors - POST".
        offset = 0
        limit = 50
        more = False
        results = []
        while offset == 0 or more is True:
            if int(time.time() - self.token_timer) > self.token_limit:
                self.extend_login()
            requ_action = action
            if paginated:
                requ_url = 'https://%s/%s?limit=%s&offset=%s' % (self.api, endpoint, limit, offset)
            else:
                requ_url = 'https://%s/%s' % (self.api, endpoint)
            requ_headers = {'Content-Type': 'application/json'}
            if self.token:
                requ_headers['authorization'] = self.token
            requ_params = query_params
            if body_params:
                requ_data = json.dumps(body_params)
            else:
                requ_data = body_params
            api_response = requests.request(requ_action, requ_url, headers=requ_headers, params=requ_params, data=requ_data, verify=self.ca_bundle)
            if self.debug:
                print('API Respose Status Code: %s' % api_response.status_code)
            if api_response.status_code in self.retry_status_codes:
                for _ in range(1, self.retry_limit):
                    time.sleep(self.retry_pause)
                    api_response = requests.request(requ_action, requ_url, headers=requ_headers, params=query_params, data=requ_data, verify=self.ca_bundle)
                    if api_response.ok:
                        break # retry loop
            if api_response.ok:
                try:
                    result = json.loads(api_response.content)
                except ValueError:
                    self.logger.error('API: (%s) responded with no response, with query %s and body params: %s' % (requ_url, query_params, body_params))
                    return None
                if paginated:
                    results.extend(result['data'])
                    if 'hasNext' in result:
                        if self.debug:
                            print('Retrieving Next Page of Results')
                        offset += limit
                        more = result['hasNext']
                    else:
                        return results
                else:
                    return result
            else:
                if force:
                    self.logger.error('API: (%s) responded with an error: (%s), with query %s and body params: %s' % (requ_url, api_response.status_code, query_params, body_params))
                    return None
                self.error_and_exit(api_response.status_code, 'API (%s) responded with an error and this response:\n%s' % (requ_url, api_response.text))
        return results

    # Exit handler (Error).

    @classmethod
    def error_and_exit(cls, error_code, error_message=None, system_message=None):
        print()
        print()
        print('Status Code: %s' % error_code)
        if error_message is not None:
            print(error_message)
        if system_message is not None:
            print(system_message)
        print()
        sys.exit(1)
