""" Prisma Cloud Compute API Images Endpoints Class """

import json
import urllib.parse

# Credentials (Manage > Authentication > Credentials store)


class CredentialsPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Credentials Endpoints Class """

    def credential_list_read(self):
        return self.execute_compute('GET', '/api/v1/credentials')

    def credential_list_create(self, id, cloud_type, secret, description):
        body = {
            'secret': secret,
            'serviceAccount': {},
            'type': cloud_type,
            'description': description,
            'skipVerify': False,
            '_id': id
        }
        return self.execute_compute(
            'POST', 'api/v1/credentials?project=Central+Console',
            body_params=body
        )

    def credential_list_delete(self, cred):
        return self.execute_compute(
            'DELETE', '/api/v1/credentials/%s' % urllib.parse.quote(cred)
        )
