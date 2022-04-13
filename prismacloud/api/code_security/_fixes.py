""" Prisma Cloud Code Security Fixes Endpoints Class """

# Fixes

class FixesPrismaCloudAPICodeSecurityMixin:
    """ Prisma Cloud Code Security API Fixes Endpoints Class """

    def fixes_list(self, body_params):
        return self.execute_code_security('POST', 'code/api/v1/fixes/checkov', body_params=body_params)
