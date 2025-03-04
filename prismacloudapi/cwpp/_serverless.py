class ServerlessPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute Serverless Endpoints Class """

    # Get serverless function scan results
    def serverless_list_read(self, query_params=None):
        return self.execute_compute_paginated('GET', 'api/v1/serverless', query_params=query_params)

    # Download serverless function scan results
    def serverless_download(self, query_params=None):
        return self.execute_compute('GET', 'api/v1/serverless/download', query_params=query_params)

    def serverless_get_function_names(self, query_params=None):
        """
        Get Serverless Function Names
        """
        return self.execute_compute_paginated('GET', 'api/v1/serverless/names', query_params=query_params)

    # Start serverless function scan
    def serverless_start_scan(self):
        result = self.execute_compute('POST', 'api/v1/serverless/scan')
        return result
   
    # Stop serverless function scan
    def serverless_stop_scan(self):
        result = self.execute_compute('POST', 'api/v1/serverless/stop')
        return result
 