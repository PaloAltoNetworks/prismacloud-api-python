""" Prisma Cloud Code Security Repositories Endpoints Class """

# Repositories

class RepositoriesPrismaCloudAPIPCCSMixin:
    """ Prisma Cloud Code Security API Repositories Endpoints Class """

    def repositories_list_read(self, query_params=None):
        return self.execute_code_security('GET', 'code/api/v1/repositories', query_params=query_params)

    def repository_name(self, body_params=None):
        return self.execute_code_security('POST', 'code/api/v1/repositories/query', body_params=body_params)

    def repository_branches(self, query_params=None):
        return self.execute_code_security('GET', 'code/api/v1/repositories/branches', query_params=query_params)

    def repositories_update(self, body_params):
        return self.execute_code_security('POST', 'code/api/v1/repositories', body_params=body_params)

    def repositories_list_read_v2(self, query_params=None):
        return self.execute_code_security('GET', 'code/api/v2/repositories', query_params=query_params)
