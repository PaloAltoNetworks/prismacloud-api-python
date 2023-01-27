""" Prisma Cloud Compute API Policies Endpoints Class """

# Credentials (Defend > Compliance)

class PoliciesPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Credentials Endpoints Class """

    def policies_cloud_platforms_read(self):
        return self.execute_compute('GET', 'api/v1/policies/cloud-platforms')

    def policies_cloud_platforms_write(self, body_params):
        return self.execute_compute('PUT', 'api/v1/policies/cloud-platforms', body_params=body_params)

    # These implement multiple endpoints. See: https://prisma.pan.dev/api/cloud/cwpp/policies

    def policies_read(self, policy_path):
        return self.execute_compute('GET', 'api/v1/policies/%s' % policy_path)

    def policies_write(self, policy_path, body_params):
        return self.execute_compute('PUT', 'api/v1/policies/%s' % policy_path, body_params=body_params)

    def policies_delete(self, policy_path):
        return self.execute_compute('PUT', 'api/v1/policies/%s' % policy_path, body_params={})
