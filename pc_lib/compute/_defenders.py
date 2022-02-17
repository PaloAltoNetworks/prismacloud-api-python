""" Prisma Cloud Compute API Defenders Endpoints Class """

# Containers

class DefendersPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Defenders Endpoints Class """

    def defenders_names_list_read(self, query_params=None):
        logs = self.execute_compute('GET', 'api/v1/defenders/names', query_params=query_params, paginated=True)
        return logs
