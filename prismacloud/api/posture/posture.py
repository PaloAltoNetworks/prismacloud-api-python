""" Requests and Output """

import json
import sys
import time

import requests

class PrismaCloudAPIMixin():
    """ Requests and Output """

    def suppress_warnings_when_verify_false(self):
        if self.verify is False:
            # Pylint Issue #4584
            # pylint: disable=no-member
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    def login(self, url=None):
        self.suppress_warnings_when_verify_false()
        if not url:
            url = 'https://%s/login' % self.api
        action = 'POST'
        request_headers = {'Content-Type': 'application/json'}
        body_params_json = json.dumps({'username': self.identity, 'password': self.secret})
        api_response = requests.request(action, url, headers=request_headers, data=body_params_json, verify=self.verify)
        if api_response.status_code in self.retry_status_codes:
            for exponential_wait in self.retry_waits:
                time.sleep(exponential_wait)
                api_response = requests.request(action, url, headers=request_headers, data=body_params_json, verify=self.verify)
                if api_response.ok:
                    break # retry loop
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token')
            self.token_timer = time.time()
        else:
            self.error_and_exit(api_response.status_code, 'API (%s) responded with an error\n%s' % (url, api_response.text))
        if self.debug:
            print('New API Token: %s' % self.token)

    def extend_login(self):
        self.suppress_warnings_when_verify_false()
        url = 'https://%s/auth_token/extend' % self.api
        action = 'GET'
        request_headers = {'Content-Type': 'application/json', 'x-redlock-auth': self.token}
        api_response = requests.request(action, url, headers=request_headers, verify=self.verify)
        if api_response.status_code in self.retry_status_codes:
            for exponential_wait in self.retry_waits:
                time.sleep(exponential_wait)
                api_response = requests.request(action, url, headers=request_headers, verify=self.verify)
                if api_response.ok:
                    break # retry loop
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token')
            self.token_timer = time.time()
        else:
            self.error_and_exit(api_response.status_code, 'API (%s) responded with an error\n%s' % (url, api_response.text))
        if self.debug:
            print('Extending API Token')

    # pylint: disable=too-many-arguments, too-many-branches, too-many-locals
    def execute(self, action, endpoint, query_params=None, body_params=None, request_headers=None, force=False, paginated=False):
        self.suppress_warnings_when_verify_false()
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
            url = 'https://%s/%s' % (self.api, endpoint)
            if not request_headers:
                request_headers = {'Content-Type': 'application/json'}
            if self.token:
                request_headers['x-redlock-auth'] = self.token
            body_params_json = json.dumps(body_params)
            api_response = requests.request(action, url, headers=request_headers, params=query_params, data=body_params_json, verify=self.verify)
            if self.debug:
                print('API Response Status Code: %s' % api_response.status_code)
            if api_response.status_code in self.retry_status_codes:
                for exponential_wait in self.retry_waits:
                    time.sleep(exponential_wait)
                    api_response = requests.request(action, url, headers=request_headers, params=query_params, data=body_params_json, verify=self.verify)
                    if api_response.ok:
                        break # retry loop
            if api_response.ok:
                if not api_response.content:
                    return None
                if api_response.headers.get('Content-Type') == 'text/csv':
                    return api_response.content.decode('utf-8')
                try:
                    result = json.loads(api_response.content)
                    if result is None:
                        self.logger.error('JSON returned None, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                        if force:
                            return results # or continue
                        self.error_and_exit(api_response.status_code, 'JSON returned None, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                except ValueError:
                    self.logger.error('JSON raised ValueError, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                    if force:
                        return results # or continue
                    self.error_and_exit(api_response.status_code, 'JSON raised ValueError, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
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
                self.logger.error('API: (%s) responded with a status of: (%s), with query: (%s) and body params: (%s)' % (url, api_response.status_code, query_params, body_params))
                if force:
                    return results
                self.error_and_exit(api_response.status_code, 'API: (%s) with query params: (%s) and body params: (%s) responded with an error and this response:\n%s' % (url, query_params, body_params, api_response.text))
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
