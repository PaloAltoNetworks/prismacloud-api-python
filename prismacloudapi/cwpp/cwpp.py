""" Requests and Output """

import json
import time

import requests

class PrismaCloudAPICWPPMixin():
    """ Requests and Output """

    def login_compute(self):
        self.suppress_warnings_when_verify_false()
        # CWP
        url = f'https://{self.api_compute}/api/v1/authenticate'
        # remove previous tokens
        if 'Authorization' in self.session_compute.headers:
            del self.session_compute.headers['Authorization']
        body_params_json = json.dumps({'username': self.identity, 'password': self.secret})
        api_response = self.session_compute.post(url, data=body_params_json, verify=self.verify, timeout=self.timeout)
        if api_response.ok:
            api_response = api_response.json()
            self.token_compute = api_response.get('token')
            self.token_compute_timer = time.time()
            self.session_compute.headers['Authorization'] = f"Bearer {self.token_compute}"
        else:
            self.error_and_exit(api_response.status_code,
                                'API (%s) responded with an error\n%s' % (url, api_response.text))

    def check_extend_login_compute(self):
        # There is no extend for CWP, just logon again.
        if not self.token_compute or (int(time.time() - self.token_compute_timer) > self.token_limit):
            self.token_compute = None
            self.debug_print('Extending CWPP API Token')
            self.login_compute()

    # def _check_

    # pylint: disable=too-many-arguments,too-many-branches,too-many-locals,too-many-statements
    def execute_compute(self, action, endpoint, query_params=None, body_params=None):
        self.suppress_warnings_when_verify_false()
        self.check_extend_login_compute()
        if body_params:
            body_params_json = json.dumps(body_params)
        else:
            body_params_json = None
        # Endpoints that return large numbers of results use a 'Total-Count' response header.
        # Pagination is via query parameters for both GET and POST, and the limit has a maximum of 50.
        url = 'https://%s/%s' % (self.api_compute, endpoint)
        self.debug_print('API URL: %s' % url)
        self.debug_print('API Request Headers: (%s)' % self.session_compute.headers)
        self.debug_print('API Query Params: %s' % query_params)
        self.debug_print('API Body Params: %s' % body_params_json)
        api_response = self.session_compute.request(action, url, params=query_params, data=body_params_json, verify=self.verify, timeout=self.timeout)
        self.debug_print('API Response Status Code: (%s)' % api_response.status_code)
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
                result = api_response.json()
            except ValueError:
                self.logger.error('JSON raised ValueError, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                self.error_and_exit(api_response.status_code, 'JSON raised ValueError, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
            return result
        else:
            self.logger.error('API: (%s) responded with a status of: (%s), with query: (%s) and body params: (%s)' % (url, api_response.status_code, query_params, body_params))
            self.error_and_exit(api_response.status_code, 'API: (%s) with query params: (%s) and body params: (%s) responded with an error and this response:\n%s' % (url, query_params, body_params, api_response.text))
        return

    def execute_compute_paginated(self, action, endpoint, query_params=None, body_params=None):
        self.suppress_warnings_when_verify_false()
        self.check_extend_login_compute()
        if body_params:
            body_params_json = json.dumps(body_params)
        else:
            body_params_json = None
        # Endpoints that return large numbers of results use a 'Total-Count' response header.
        # Pagination is via query parameters for both GET and POST, and the limit has a maximum of 100.
        offset = 0
        limit = 100
        more = True
        while more is True:
            self.check_extend_login_compute()
            url = f'https://{self.api_compute}/{endpoint}?limit={limit}&offset={offset}'
            self.debug_print('API URL: %s' % url)
            self.debug_print('API Request Headers: (%s)' % self.session_compute.headers)
            self.debug_print('API Query Params: %s' % query_params)
            self.debug_print('API Body Params: %s' % body_params_json)
            api_response = self.session_compute.request(action, url, params=query_params, data=body_params_json, verify=self.verify, timeout=self.timeout)
            self.debug_print('API Response Status Code: (%s)' % api_response.status_code)
            self.debug_print('API Response Headers: (%s)' % api_response.headers)
            if api_response.ok:
                if not api_response.content:
                    return
                if api_response.headers.get('Content-Type') == 'application/x-gzip':
                    # return api_response.content
                    raise RuntimeError("please use .execute instead of execute_paginated")
                if api_response.headers.get('Content-Type') == 'text/csv':
                    # return api_response.content.decode('utf-8')
                    raise RuntimeError("please use .execute instead of execute_paginated")
                try:
                    results = api_response.json()
                except ValueError:
                    self.logger.error('JSON raised ValueError, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                    self.error_and_exit(api_response.status_code, 'JSON raised ValueError, API: (%s) with query params: (%s) and body params: (%s) parsing response: (%s)' % (url, query_params, body_params, api_response.content))
                if 'Total-Count' in api_response.headers:
                    total_count = int(api_response.headers['Total-Count'])
                    self.debug_print(f'Retrieving Next Page of Results: Offset/Total Count: {offset}/{total_count}')
                else:
                    self.debug_print("No Pagination headers - please use .execute instead of execute_paginated")
                    if results:
                        yield from results
                    return
                    # raise RuntimeError("please use .execute instead of execute_paginated")
                if not results:
                    return
                self.debug_print(f"Got {len(results)} results")
                if total_count > 0:
                    yield from results
                offset += len(results)
                more = bool(offset < total_count)
            else:
                self.logger.error('API: (%s) responded with a status of: (%s), with query: (%s) and body params: (%s)' % (url, api_response.status_code, query_params, body_params))
                self.error_and_exit(api_response.status_code, 'API: (%s) with query params: (%s) and body params: (%s) responded with an error and this response:\n%s' % (url, query_params, body_params, api_response.text))
        return

    # The Compute API setting is optional.

    def validate_api_compute(self):
        if not self.api_compute:
            self.error_and_exit(500, 'Please specify a Prisma Cloud Compute API URL.')

    # Exit handler (Error).

    @classmethod
    def error_and_exit(cls, error_code, error_message='', system_message=''):
        raise SystemExit('\n\nStatus Code: %s\n%s\n%s\n' % (error_code, error_message, system_message))

    # various API

    def version(self):
        return self.execute_compute('GET', 'api/v1/version')

    def ping(self):
        # unauthenticated call
        return self.session_compute.get(f'https://{self.api_compute}/api/v1/_ping').text
