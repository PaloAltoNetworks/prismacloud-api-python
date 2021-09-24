""" Requests and Output """

from __future__ import print_function

import json
import sys
import time

import requests

class PrismaCloudAPIMixin():
    """ Requests and Output """

    def login(self, requ_url=None):
        if not requ_url:
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
            self.error_and_exit(api_response.status_code, 'API (%s) responded with an error\n%s' % (requ_url, api_response.text))

    def extend_login(self):
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

    # pylint: disable=too-many-arguments
    def execute(self, action, endpoint, query_params=None, body_params=None, force=False):
        if not self.token:
            self.login()
        if int(time.time() - self.token_timer) > self.token_limit:
            self.extend_login()
        requ_action = action
        requ_url = 'https://%s/%s' % (self.api, endpoint)
        requ_headers = {'Content-Type': 'application/json'}
        if self.token:
            requ_headers['x-redlock-auth'] = self.token
        requ_params = query_params
        requ_data = json.dumps(body_params)
        api_response = requests.request(requ_action, requ_url, headers=requ_headers, params=requ_params, data=requ_data, verify=self.ca_bundle)
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
        else:
            if force:
                self.logger.error('API: (%s) responded with an error: (%s), with query %s and body params: %s' % (requ_url, api_response.status_code, query_params, body_params))
                return None
            self.error_and_exit(api_response.status_code, 'API (%s) responded with an error\n%s' % (requ_url, api_response.text))
        return result

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
