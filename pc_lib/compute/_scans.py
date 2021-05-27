""" Prisma Cloud Compute API Scans Endpoints Class """

# Scans (Monitor > Vulnerabilities/Compliance > Images > CI)

class ScansPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Scans Endpoints Class """

    def scans_list_read(self, image_id=None):
        if image_id:
            images = self.execute_compute('GET', 'api/v1/scans?imageID=%s&filterBaseImage=true' % image_id)
        else:
            images = self.execute_compute('GET', 'api/v1/scans?filterBaseImage=true', paginated=True)
        return images
