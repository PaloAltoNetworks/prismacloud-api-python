""" Prisma Compute API Cloud Endpoints Class """

# Cloud

class CloudPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Cloud Endpoints Class """

    def cloud_discovery_read(self):
        return self.execute_compute('GET', 'api/v1/cloud/discovery')

    def cloud_discovery_download(self, query_params=None):
        # request_headers = {'Content-Type': 'text/csv'}
        # return self.execute_compute('GET', 'api/v1/cloud/discovery/download?', request_headers=request_headers, query_params=query_params)
        return self.execute_compute('GET', 'api/v1/cloud/discovery/download', query_params=query_params)

    def cloud_discovery_scan(self):
        return self.execute_compute('POST', 'api/v1/cloud/discovery/scan')

    def cloud_discovery_scan_stop(self):
        return self.execute_compute('POST', 'api/v1/cloud/discovery/stop')

    def cloud_discovery_vms(self, query_params=None):
        return self.execute_compute('GET', 'api/v1/cloud/discovery/vms?', query_params=query_params, paginated=True)
