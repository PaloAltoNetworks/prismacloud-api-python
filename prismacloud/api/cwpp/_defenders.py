""" Prisma Cloud Compute API Defenders Endpoints Class """

# Containers

class DefendersPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Defenders Endpoints Class """

    def defenders_list_read(self, query_params=None):
        defenders = self.execute_compute('GET', 'api/v1/defenders', query_params=query_params, paginated=True)
        return defenders

    def defenders_names_list_read(self, query_params=None):
        defenders = self.execute_compute('GET', 'api/v1/defenders/names', query_params=query_params, paginated=True)
        return defenders
