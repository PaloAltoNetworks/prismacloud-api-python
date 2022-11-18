""" Prisma Cloud Compute API Images Endpoints Class """

# Images (Monitor > Vulnerabilities/Compliance > Images > Deployed)

class RegistryPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Images Endpoints Class """

    def registry_list_read(self, image_id=None):
        if image_id:
            images = self.execute_compute('GET', 'api/v1/registry?id=%s&filterBaseImage=true' % image_id)
        else:
            images = self.execute_compute('GET', 'api/v1/registry?filterBaseImage=true', paginated=True)
        return images

    def registry_scan(self, body_params=None):
        result = self.execute_compute('POST', 'api/v1/registry/scan', body_params=body_params)
        return result
