""" Prisma Cloud Compute API Images Endpoints Class """

# Images (Monitor > Vulnerabilities/Compliance > Images > Deployed)

class ImagesPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Images Endpoints Class """

    def images_get_read(self, image_id, query_params=None):
        return self.execute_compute('GET', 'api/v1/images?id=%s' % image_id, query_params=query_params)

    def images_list_read(self, query_params=None):
        images = self.execute_compute_paginated('GET', 'api/v1/images?', query_params=query_params)
        return images

    def images_download(self, query_params=None):
        images = self.execute_compute('GET', 'api/v1/images/download?', query_params=query_params)
        return images
