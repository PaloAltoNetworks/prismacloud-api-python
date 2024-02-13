""" Prisma Cloud Compute API Images Endpoints Class """

# Images (Monitor > Vulnerabilities/Compliance > Images > Deployed)

class RegistryPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Images Endpoints Class """

    def registry_list_read(self, image_id=None):
        if image_id:
            images = self.execute_compute('GET', 'api/v1/registry?id=%s&filterBaseImage=true' % image_id)
        else:
            images = self.execute_compute('GET', 'api/v1/registry?filterBaseImage=true', paginated=True)
        return images

    def registry_list_image_names(self, query_params=None):
        result = self.execute_compute('GET', 'api/v1/registry/names?', query_params=query_params)
        return result

    def registry_scan(self, body_params=None):
        result = self.execute_compute('POST', 'api/v1/registry/scan', body_params=body_params)
        return result

    def registry_scan_select(self, body_params=None):
        result = self.execute_compute('POST', 'api/v1/registry/scan/select', body_params=body_params)
        return result
