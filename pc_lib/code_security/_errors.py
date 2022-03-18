""" Prisma Cloud Code Security Errors Endpoints Class """

# Errors

class ErrorsPrismaCloudAPICodeSecurityMixin:
    """ Prisma Cloud Code Security API Errors Endpoints Class """

    def errors_files_list(self, criteria):
        return self.execute_code_security('POST', 'code/api/v1/errors/files', body_params=criteria)

    def errors_file_list(self, criteria):
        return self.execute_code_security('POST', 'code/api/v1/errors/file', body_params=criteria, paginated=True)

    def errors_list_last_authors(self):
        return self.execute_code_security('GET', 'code/api/v1/errors/gitBlameAuthors')

    def fix_or_suppress_scan_results(self, criteria):
        return self.execute_code_security('POST', 'code/api/v1/errors/submitActions', body_params=criteria)

    def fixed_resource_code(self, criteria):
        return self.execute_code_security('POST', 'code/api/v1/errors/getFixedCode', body_params=criteria)
