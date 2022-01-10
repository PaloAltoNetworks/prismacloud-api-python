""" Prisma Cloud Compute API Policies Endpoints Class """

# Credentials (Defend > Compliance)

class PoliciesPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Credentials Endpoints Class """

    def policies_cloud_platforms_read(self):
        return self.execute_compute('GET', 'api/v1/policies/cloud-platforms')

    def policies_cloud_platforms_write(self, body):
        return self.execute_compute(
            'put', 'api/v1/policies/cloud-platforms',
            body_params=body
        )
