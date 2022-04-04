""" Prisma Cloud Compute API Statuses Endpoints Class """

class StatusPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Statuses Endpoints Class """

    def statuses_intelligence(self):
        return self.execute_compute('GET', 'api/v1/statuses/intelligence')

    def statuses_registry(self):
        return self.execute_compute('GET', 'api/v1/statuses/registry')
