""" Requests and Output """

import json
import sys
import time

import requests

class PrismaCloudAPIMixin():
    """ Requests and Output """

    def suppress_warnings_when_ca_bundle_false(self):
        if self.ca_bundle is False:
            # Pylint Issue #4584
            # pylint: disable=no-member
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    def login(self, requ_url=None):
        self.suppress_warnings_when_ca_bundle_false()
        if not requ_url:
            requ_url = 'https://%s/login' % self.api
        requ_action = 'POST'
        requ_headers = {'Content-Type': 'application/json'}
        requ_data = json.dumps({'username': self.username, 'password': self.password})
        api_response = requests.request(requ_action, requ_url, headers=requ_headers, data=requ_data, verify=self.ca_bundle)
        if api_response.status_code in self.retry_status_codes:
            for _ in range(1, self.retry_limit):
                time.sleep(self.retry_pause)
                api_response = requests.request(requ_action, requ_url, headers=requ_headers, data=requ_data, verify=self.ca_bundle)
                if api_response.ok:
                    break
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token')
            self.token_timer = time.time()
        else:
            self.error_and_exit(api_response.status_code, 'API (%s) responded with an error\n%s' % (requ_url, api_response.text))
        if self.debug:
            print('New API Token: %s' % self.token)

    def extend_login(self):
        self.suppress_warnings_when_ca_bundle_false()
        requ_url = 'https://%s/auth_token/extend' % self.api
        requ_action = 'GET'
        requ_headers = {'Content-Type': 'application/json', 'x-redlock-auth': self.token}
        api_response = requests.request(requ_action, requ_url, headers=requ_headers, verify=self.ca_bundle)
        if api_response.status_code in self.retry_status_codes:
            for _ in range(1, self.retry_limit):
                time.sleep(self.retry_pause)
                api_response = requests.request(requ_action, requ_url, headers=requ_headers, verify=self.ca_bundle)
                if api_response.ok:
                    break
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token')
            self.token_timer = time.time()
        else:
            self.error_and_exit(api_response.status_code, 'API (%s) responded with an error\n%s' % (requ_url, api_response.text))
        if self.debug:
            print('Extending API Token')

    # pylint: disable=too-many-arguments, too-many-locals
    def execute(self, action, endpoint, query_params=None, body_params=None, force=False, paginated=False):
        self.suppress_warnings_when_ca_bundle_false()
        if not self.token:
            self.login()
        if int(time.time() - self.token_timer) > self.token_limit:
            self.extend_login()
        # Endpoints that return large numbers of results use a 'nextPageToken' (and a 'totalRows') key.
        # Pagination appears to be specific to "List Alerts V2 - POST" and the limit has a maximum of 10000.
        more = True
        results = []
        while more is True:
            if int(time.time() - self.token_timer) > self.token_limit:
                self.extend_login()
            requ_action = action
            requ_url = 'https://%s/%s' % (self.api, endpoint)
            requ_headers = {'Content-Type': 'application/json'}
            if self.token:
                requ_headers['x-redlock-auth'] = self.token
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
                    if api_response.content:
                        self.logger.error('API: (%s) responded with an error: (%s), with query %s and body params: %s' % (requ_url, api_response.status_code, query_params, body_params))
                    return None
                if paginated:
                    results.extend(result['items'])
                    if 'nextPageToken' in result and result['nextPageToken']:
                        if self.debug:
                            print('Retrieving Next Page of Results')
                        body_params = {'pageToken': result['nextPageToken']}
                        more = True
                    else:
                        more = False
                else:
                    return result
            else:
                if force:
                    self.logger.error('API: (%s) responded with an error: (%s), with query %s and body params: %s' % (requ_url, api_response.status_code, query_params, body_params))
                    return None
                self.error_and_exit(api_response.status_code, 'API (%s) responded with an error\n%s' % (requ_url, api_response.text))
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

    # Output counted errors.

    def error_report(self):
        if self.logger.error.counter > 0:
            print('API responded with (%s) error(s): details logged to: (%s)' % (self.logger.error.counter, self.error_log))

    # Optionally output progress.

    @classmethod
    def progress(cls, txt=None):
        if txt:
            print(txt)
