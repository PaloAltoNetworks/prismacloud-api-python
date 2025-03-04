""" Prisma Cloud Code Security Scans Endpoints Class """

# Scans

class PackagesPrismaCloudAPIPCCSMixin:
    """ Prisma Cloud Code Security API Packages Endpoints Class """

    def list_cves_per_package(self, package_uuid, query_params=None):
        return self.execute_code_security('GET', 'code/api/v1/vulnerabilities/packages/%s/cves' % package_uuid, query_params=query_params)
