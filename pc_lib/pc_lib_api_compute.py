import json
import time

import requests

from .pc_lib_utility import PrismaCloudUtility

# --Description-- #

# Prisma Cloud API (Compute) library.

# --Class Methods-- #

class PrismaCloudAPICompute():

    # TwistLock API. See pc_lib_api for RedLock API methods.

    def execute_compute(self, action, endpoint, query_params=None, body_params=None, force=False, paginated=False):
        if not self.token:
            self.login()
        # Endpoints that have the potential to return large numbers of results return a 'Total-Count' response header.
        offset = 0
        limit = 50
        total = 0
        results = []
        while offset == 0 or offset < total:
            if int(time.time() - self.token_timer) > self.token_limit:
                self.extend_token()
            requ_action = action
            if paginated:
                requ_url = 'https://%s/%s&limit=%s&offset=%s' % (self.api_compute, endpoint, limit, offset)
            else:
                requ_url = 'https://%s/%s' % (self.api_compute, endpoint)
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
                if 'Total-Count' in api_response.headers:
                    results.extend(result)
                    total = int(api_response.headers['Total-Count'])
                else:
                    return result
            else:
                if force:
                    self.logger.error('API: (%s) responded with an error: (%s), with query %s and body params: %s' % (requ_url, api_response.status_code, query_params, body_params))
                    return None
                PrismaCloudUtility.error_and_exit(self, api_response.status_code, 'API (%s) responded with an error\n%s' % (requ_url, api_response.text))
            offset += limit
        return results

    # The Compute API setting is optional.

    def validate_api_compute(self):
        if not self.api_compute:
            PrismaCloudUtility.error_and_exit(self, 500, 'Please specify a Prisma Cloud Compute Base URL.')

    # --API Endpoints-- #

    def statuses_intelligence(self):
        return self.execute_compute('GET', 'api/v1/statuses/intelligence')

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
    Images (Monitor > Vulnerabilities/Compliance > Images > Deployed)

    [x] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    """

    def images_list_read(self, image_id=None):
        if image_id:
            images = self.execute_compute('GET', 'api/v1/images?id=%s&filterBaseImage=true' % image_id)
        else:
            images = self.execute_compute('GET', 'api/v1/images?filterBaseImage=true', paginated=True)
        return images

    """
    Scans (Monitor > Vulnerabilities/Compliance > Images > CI)

    [x] LIST
    [ ] CREATE
    [ ] READ
    [ ] UPDATE
    [ ] DELETE
    """

    def scans_list_read(self, image_id=None):
        if image_id:
            images = self.execute_compute('GET', 'api/v1/scans?imageID=%s&filterBaseImage=true' % image_id)
        else:
            images = self.execute_compute('GET', 'api/v1/scans?filterBaseImage=true', paginated=True)
        return images
