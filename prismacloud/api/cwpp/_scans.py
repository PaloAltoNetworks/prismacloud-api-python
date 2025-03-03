""" Prisma Cloud Compute API Scans Endpoints Class """

# Scans (Monitor > Vulnerabilities/Compliance > Images > CI)

class ScansPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Scans Endpoints Class """

    def scans_get(self, image_id):
        return self.execute_compute('GET', 'api/v1/scans?imageID=%s&filterBaseImage=true' % image_id)

    def scans_list_read(self):
        images = self.execute_compute_paginated('GET', 'api/v1/scans?filterBaseImage=true', paginated=True)
        return images

    def scans_download(self, query_params=None):
        scans = self.execute_compute('GET', 'api/v1/scans/download?', query_params=query_params)
        return scans
