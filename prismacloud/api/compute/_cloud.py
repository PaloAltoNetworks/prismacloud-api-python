""" Prisma Compute API Cloud Endpoints Class """

# Cloud

class CloudPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Cloud Endpoints Class """

    def cloud_discovery_read(self):
        return self.execute_compute('GET', 'api/v1/cloud/discovery')
