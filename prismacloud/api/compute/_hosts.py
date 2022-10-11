""" Prisma Cloud Compute API Hosts Endpoints Class """

# Containers

class HostsPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Hosts Endpoints Class """

    # Running hosts table in Monitor > Vulnerabilities > Hosts > Running Hosts
    def hosts_list_read(self, query_params=None):
        hosts = self.execute_compute('GET', 'api/v1/hosts', query_params=query_params, paginated=True)
        return hosts

    def hosts_info_list_read(self, query_params=None):
        hosts = self.execute_compute('GET', 'api/v1/hosts/info', query_params=query_params, paginated=True)
        return hosts

    def hosts_download(self, query_params=None):
        hosts = self.execute_compute('GET', 'api/v1/hosts/download?', query_params=query_params)
        return hosts

    def hosts_scan(self):
        result = self.execute_compute('POST', 'api/v1/hosts/scan')
        return result
