class StatusPrismaCloudAPIComputeMixin:
    def statuses_intelligence(self):
        return self.execute_compute('GET', 'api/v1/statuses/intelligence')
