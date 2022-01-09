""" Prisma Cloud Compute API Images Endpoints Class """

import urllib.parse

# Credentials (Manage > Authentication > Credentials store)


class CredentialsPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Credentials Endpoints Class """

    def credential_list_read(self):
        return self.execute_compute('GET', 'api/v1/credentials')

    def credential_list_create(self, body):
        return self.execute_compute(
            'POST', 'api/v1/credentials?project=Central+Console',
            body_params=body
        )

    def credential_list_delete(self, cred):
        return self.execute_compute(
            'DELETE', '/api/v1/credentials/%s' % urllib.parse.quote(cred)
        )

    def credential_list_usages_read(self, cred):
        return self.execute_compute(
            'GET', '/api/v1/credentials/%s/usages' % urllib.parse.quote(cred)
        )
