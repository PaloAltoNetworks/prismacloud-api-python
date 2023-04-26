""" Prisma Cloud Code Security Errors Endpoints Class """

# Errors

class ErrorsPrismaCloudAPIPCCSMixin:
    """ Prisma Cloud Code Security API Errors Endpoints Class """

    def errors_files_list(self, criteria):
        return self.execute_code_security('POST', 'code/api/v1/errors/files', body_params=criteria)

    def errors_file_list(self, criteria):
        return self.execute_code_security('POST', 'code/api/v1/errors/file', body_params=criteria, paginated=True)

    def errors_list_last_authors(self, query_params=None):
        return self.execute_code_security('GET', 'code/api/v1/errors/gitBlameAuthors', query_params=query_params)

    def fix_or_suppress_scan_results(self, criteria):
        return self.execute_code_security('POST', 'code/api/v1/errors/submitActions', body_params=criteria)

    def fixed_resource_code(self, criteria):
        return self.execute_code_security('POST', 'code/api/v1/errors/getFixedCode', body_params=criteria)

    def resources_list(self, body_params=None):
        return self.execute_code_security('POST', 'code/api/v2/errors/branch_scan/resources', body_params=body_params)

    def policies_list(self, resource_uuid, body_params=None):
        return self.execute_code_security('POST', 'code/api/v2/errors/branch_scan/resources/%s/policies' % resource_uuid, body_params=body_params)

    def vulnerabilities_list(self, resource_uuid, query_params):
        return self.execute_code_security('GET', 'code/api/v2/summaries/resource/%s/Vulnerabilities' % resource_uuid, query_params=query_params)
