""" Requests and Output """

import json
import logging
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
            url = f'https://{self.api}/login'
        action = 'POST'
        request_headers = {'Content-Type': 'application/json'}
        # Add User-Agent to the headers
        request_headers['User-Agent'] = self.user_agent
        body_params_json = json.dumps({'username': self.identity, 'password': self.secret})
        api_response = self.session.request(action, url, headers=request_headers, data=body_params_json, verify=self.verify, timeout=self.timeout)
        # use a requests retry adapter
        # if api_response.status_code in self.retry_status_codes:
        #     for exponential_wait in self.retry_waits:
        #         time.sleep(exponential_wait)
        #         api_response = requests.request(action, url, headers=request_headers, data=body_params_json, verify=self.verify, timeout=self.timeout)
        #         if api_response.ok:
        #             break # retry loop
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token')
            self.token_timer = time.time()
        else:
            self.error_and_exit(api_response.status_code, 'API (%s) responded with an error\n%s' % (url, api_response.text))
        self.debug_print('New API Token: %s' % self.token)

    def extend_login(self):
        self.suppress_warnings_when_verify_false()
        self.debug_print('Extending API Token')
        url = f'https://{self.api}/auth_token/extend'
        action = 'GET'
        request_headers = {'Content-Type': 'application/json', 'x-redlock-auth': self.token}
        # Add User-Agent to the headers
        request_headers['User-Agent'] = self.user_agent
        api_response = self.session.request(action, url, headers=request_headers, verify=self.verify, timeout=self.timeout)
        if api_response.ok:
            api_response = json.loads(api_response.content)
            self.token = api_response.get('token')
            self.token_timer = time.time()
        else:
            logging.warning(f'HTTP error code {api_response.status_code} - API ({url}) responded with an error - lets try to login again\n {api_response.text}')
            # try to login again
            self.login()

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
            if body_params:
                body_params_json = json.dumps(body_params)
            else:
                body_params_json = None
            self.debug_print('API URL: %s' % url)
            self.debug_print('API Request Headers: (%s)' % request_headers)
            self.debug_print('API Query Params: %s' % query_params)
            self.debug_print('API Body Params: %s' % body_params_json)
            # Add User-Agent to the headers
            request_headers['User-Agent'] = self.user_agent
            api_response = self.session.request(action, url, headers=request_headers, params=query_params, data=body_params_json, verify=self.verify, timeout=self.timeout)
            self.debug_print('API Response Status Code: %s' % api_response.status_code)
            self.debug_print('API Response Headers: (%s)' % api_response.headers)
            # if api_response.status_code in self.retry_status_codes:
            #     for exponential_wait in self.retry_waits:
            #         time.sleep(exponential_wait)
            #         api_response = requests.request(action, url, headers=request_headers, params=query_params, data=body_params_json, verify=self.verify, timeout=self.timeout)
            #         if api_response.ok:
            #             break # retry loop
            if api_response.ok:
                if not api_response.content:
                    return None
                if api_response.headers.get('Content-Type') == 'application/x-gzip':
                    return api_response.content
                if api_response.headers.get('Content-Type') == 'text/csv':
                    return api_response.content.decode('utf-8')
                try:
                    result = json.loads(api_response.content)
                    #if result is None:
                    #    self.logger.error('JSON returned None, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                    #    if force:
                    #        return results # or continue
                    #    self.error_and_exit(api_response.status_code, 'JSON returned None, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                except ValueError:
                    self.logger.error('JSON raised ValueError, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                    if force:
                        return results # or continue
                    self.error_and_exit(api_response.status_code, 'JSON raised ValueError, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                if paginated:
                    results.extend(result['items'])
                    if 'nextPageToken' in result and result['nextPageToken']:
                        self.debug_print('Retrieving Next Page of Results')
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
    def error_and_exit(cls, error_code, error_message='', system_message=''):
        raise SystemExit('\n\nStatus Code: %s\n%s\n%s\n' % (error_code, error_message, system_message))

    # Output counted errors.

    def error_report(self):
        if self.logger.error.counter > 0:
            print('API responded with (%s) error(s): details logged to: (%s)' % (self.logger.error.counter, self.error_log))

    # Optionally output progress.

    @classmethod
    def progress(cls, txt=None):
        if txt:
            print(txt)
