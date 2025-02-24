""" Prisma Cloud Compute API Containers Endpoints Class """

# Containers

class ContainersPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Containers Endpoints Class """

    def containers_list_read(self, image_id=None, query_params=None):
        if image_id:
            containers = self.execute_compute('GET', 'api/v1/containers?imageId=%s' % image_id, query_params=query_params, paginated=True)
        else:
            containers = self.execute_compute('GET', 'api/v1/containers?', query_params=query_params, paginated=True)
        return containers

    def containers_download(self, query_params=None):
        containers = next(self.execute_compute('GET', 'api/v1/containers/download?', query_params=query_params))
        return containers
