""" Requests and Output """

import json
import sys
import time

import requests

class PrismaCloudAPIComputeMixin():
    """ Requests and Output """

    def login_compute(self):
        if self.api:
            # Login via CSPM.
            self.login()
        elif self.api_compute:
            # Login via CWP.
            self.login('https://%s/api/v1/authenticate' % self.api_compute)
        else:
            self.error_and_exit(418, "Specify a Prisma Cloud API/UI Base URL or Prisma Cloud Compute API Base URL")
        if self.debug:
            print('New API Token: %s' % self.token)

    def extend_login_compute(self):
        # There is no extend for CWP, just logon again.
        if self.debug:
            print('Extending API Token')
        self.login_compute()

    # pylint: disable=too-many-arguments,too-many-branches,too-many-locals,too-many-statements
    def execute_compute(self, action, endpoint, query_params=None, body_params=None, force=False, paginated=False):
        self.suppress_warnings_when_ca_bundle_false()
        if not self.token:
            self.login_compute()
        # Endpoints that return large numbers of results use a 'Total-Count' response header.
        # Pagination is via query parameters for both GET and POST, and the limit has a maximum of 50.
        offset = 0
        limit = 50
        more = False
        results = []
        while offset == 0 or more is True:
            if int(time.time() - self.token_timer) > self.token_limit:
                self.extend_login_compute()
            requ_action = action
            if paginated:
                requ_url = 'https://%s/%s?limit=%s&offset=%s' % (self.api_compute, endpoint, limit, offset)
            else:
                requ_url = 'https://%s/%s' % (self.api_compute, endpoint)
            requ_headers = {'Content-Type': 'application/json'}
            if self.token:
                if self.api:
                    # Authenticate via CSPM
                    requ_headers['x-redlock-auth'] = self.token
                else:
                    # Authenticate via CWP
                    requ_headers['Authorization'] = "Bearer %s" % self.token
            requ_params = query_params
            requ_data = json.dumps(body_params)
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
                if 'Total-Count' in api_response.headers:
                    if self.debug:
                        print('Retrieving Next Page of Results: Offset/Total Count: %s/%s' % (offset, api_response.headers['Total-Count']))
                    total_count = int(api_response.headers['Total-Count'])
                    if total_count > 0:
                        results.extend(result)
                    offset += limit
                    more = bool(offset < total_count)
                else:
                    return result
            else:
                if force:
                    self.logger.error('API: (%s) responded with an error: (%s), with query %s and body params: %s' % (requ_url, api_response.status_code, query_params, body_params))
                    return None
                self.error_and_exit(api_response.status_code, 'API (%s) responded with an error and this response:\n%s' % (requ_url, api_response.text))
        return results

    # The Compute API setting is optional.

    def validate_api_compute(self):
        if not self.api_compute:
            self.error_and_exit(500, 'Please specify a Prisma Cloud Compute API Base URL.')

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
