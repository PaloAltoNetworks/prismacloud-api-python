class Status_PrismaCloudAPICompute_Mixin:
    def statuses_intelligence(self):
        return self.execute_compute('GET', 'api/v1/statuses/intelligence')
