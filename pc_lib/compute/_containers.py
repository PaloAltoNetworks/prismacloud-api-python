""" Prisma Cloud Compute API Containers Endpoints Class """

# Containers

class ContainersPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Images Endpoints Class """

    def containers_list_read(self, image_id=None):
        if image_id:
            containers = self.execute_compute('GET', 'api/v1/containers?imageId=%s' % image_id, paginated=True)
        else:
            containers = self.execute_compute('GET', 'api/v1/containers?', paginated=True)
        return containers
