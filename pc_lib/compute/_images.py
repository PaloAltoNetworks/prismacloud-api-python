""" Prisma Cloud Compute API Images Endpoints Class """

# Images (Monitor > Vulnerabilities/Compliance > Images > Deployed)

class ImagesPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Images Endpoints Class """

    def images_list_read(self, image_id=None, query_params=None):
        if image_id:
            images = self.execute_compute('GET', 'api/v1/images?id=%s' % image_id, query_params=query_params)
        else:
            images = self.execute_compute('GET', 'api/v1/images?', query_params=query_params, paginated=True)
        return images
