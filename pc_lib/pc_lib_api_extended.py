from .pc_lib_utility import PrismaCloudUtility

import concurrent.futures
import json
import requests
import time

# --Description-- #

# Prisma Cloud API Extended library.

# --Class Methods-- #

class PrismaCloudAPIExtended():

    # --Threading-- #

    def threaded_policy_get(self, policy_current):
        self.progress('Getting Policy: %s' % policy_current['name'])
        return self.policy_get(policy_current['policyId'])

    def threaded_saved_search_get(self, policy_current):
        self.progress('Getting Saved Search: %s' % policy_current['name'])
        return self.saved_search_get(policy_current['rule']['criteria'])

    # --Main-- #

    def export_policies_with_saved_searches(self, policy_list_current):
        result = {'policies': {}, 'searches': {}}
        thread_pool_executor = concurrent.futures.ThreadPoolExecutor(self.max_workers)
        self.progress('API - Getting the Custom Policies ...')
        futures = []
        for policy_current in policy_list_current:
            self.progress('Scheduling Policy Request: %s' % policy_current['name'])
            futures.append(thread_pool_executor.submit(self.threaded_policy_get, policy_current))
        concurrent.futures.wait(futures)
        for future in concurrent.futures.as_completed(futures):
            policy_current = future.result()
            result['policies'][policy_current['policyId']] = policy_current
        self.progress('Done.')
        self.progress()
        self.progress('API - Getting the Custom Policies Saved Searches ...')
        futures = []
        for policy_current in policy_list_current:
            if not 'parameters' in policy_current['rule']:
                continue
            if not 'savedSearch' in policy_current['rule']['parameters']:
                continue
            if policy_current['rule']['parameters']['savedSearch'] == 'true':
                self.progress('Scheduling Saved Search Request: %s' % policy_current['name'])
                futures.append(thread_pool_executor.submit(self.threaded_saved_search_get, policy_current))
        concurrent.futures.wait(futures)
        for future in concurrent.futures.as_completed(futures):
            saved_search = future.result()
            result['searches'][saved_search['id']] = saved_search
        self.progress('Done.')
        self.progress()
        return result
