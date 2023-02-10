""" Prisma Cloud Code Security Checkov Version Endpoint Class """

# Checkov Version

class CheckovVersionPrismaCloudAPIPCCSMixin:
    """ Prisma Cloud Code Security API Checkov Version Endpoint Class """

    def checkov_version(self):
        version = self.execute_code_security('GET', 'code/api/v1/checkovVersion')
        return version
