""" Prisma Cloud API Endpoints Aggregation Class """

import concurrent.futures

# TODO: Rename this class ...

class ExtendedPrismaCloudAPIMixin():
    """ Prisma Cloud API Endpoints Aggregation Class """

    def get_policies_with_saved_searches(self, policy_list_current):
        result = {'policies': {}, 'searches': {}}
        if not policy_list_current:
            return result
        # pylint: disable=consider-using-with
        thread_pool_executor = concurrent.futures.ThreadPoolExecutor(self.max_workers)
        self.progress('API - Getting the Custom Policies ...')
        futures = []
        for policy_current in policy_list_current:
            self.progress('Scheduling Policy Request: %s' % policy_current['name'])
            thread_progress = 'Getting Policy: %s' % policy_current['name']
            futures.append(thread_pool_executor.submit(self.policy_read, policy_current['policyId'], message=thread_progress))
        concurrent.futures.wait(futures)
        for future in concurrent.futures.as_completed(futures):
            policy_current = future.result()
            result['policies'][policy_current['policyId']] = policy_current
        self.progress('Done.')
        self.progress(' ')
        self.progress('API - Getting the Custom Policies Saved Searches ...')
        futures = []
        for policy_current in policy_list_current:
            if not 'parameters' in policy_current['rule']:
                continue
            if not 'savedSearch' in policy_current['rule']['parameters']:
                continue
            if policy_current['rule']['parameters']['savedSearch'] == 'true':
                self.progress('Scheduling Saved Search Request: %s' % policy_current['name'])
                thread_progress = 'Getting Saved Search: %s' % policy_current['name']
                futures.append(thread_pool_executor.submit(self.saved_search_read, policy_current['rule']['criteria'], message=thread_progress))
        concurrent.futures.wait(futures)
        for future in concurrent.futures.as_completed(futures):
            saved_search = future.result()
            result['searches'][saved_search['id']] = saved_search
        self.progress('Done.')
        self.progress(' ')
        return result

    def get_cloud_resources(self, cloud_account_resource_list):
        result = []
        if not cloud_account_resource_list:
            return result
        # pylint: disable=consider-using-with
        thread_pool_executor = concurrent.futures.ThreadPoolExecutor(self.max_workers)
        self.progress('API - Getting the Resources ...')
        futures = []
        for cloud_account_resource in cloud_account_resource_list:
            if not 'rrn' in cloud_account_resource:
                continue
            self.progress('Scheduling Resource Request: %s' % cloud_account_resource['rrn'])
            thread_progress = 'Getting Resource: %s' % cloud_account_resource['rrn']
            futures.append(thread_pool_executor.submit(self.resource_read, body_params={'rrn': cloud_account_resource['rrn']}, force=True, message=thread_progress))
        concurrent.futures.wait(futures)
        for future in concurrent.futures.as_completed(futures):
            resource = future.result()
            if resource:
                result.append(resource)
        self.progress('Done.')
        return result
