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

    def threaded_resource_get(self, resource):
        self.progress('Getting Resource: %s' % resource['rrn'])
        resource = self.resource_get(body_params={'rrn': resource['rrn']}, force=True)
        #"""
        networks = self.resource_network_get(body_params={'rrn': resource['rrn']}, force=True)
        if resource and networks:
            resource['prisma_resource_network'] = networks
        #"""
        return resource

    # --Main-- #

    def export_policies_with_saved_searches(self, policy_list_current):
        result = {'policies': {}, 'searches': {}}
        if not policy_list_current:
            return result
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

    def export_resources(self, cloud_account_resource_list):
        result = []
        if not cloud_account_resource_list:
            return result
        thread_pool_executor = concurrent.futures.ThreadPoolExecutor(self.max_workers)
        self.progress('API - Getting the Resources ...')
        futures = []
        for cloud_account_resource in cloud_account_resource_list:
            self.progress('Scheduling Resource Request: %s' % cloud_account_resource['rrn'])
            futures.append(thread_pool_executor.submit(self.threaded_resource_get, cloud_account_resource))
        concurrent.futures.wait(futures)
        for future in concurrent.futures.as_completed(futures):
            resource = future.result()
            if resource:
                result.append(resource)
        self.progress('Done.')
        return result
