""" Prisma Cloud Code Security Scans Endpoints Class """

# Scans

class ScansPrismaCloudAPICodeSecurityMixin:
    """ Prisma Cloud Code Security API Scans Endpoints Class """

    def scan(self):
        return self.execute_code_security('POST', 'code/api/v1/scans/integrations')
