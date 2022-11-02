""" Prisma Cloud Compute API Collections Endpoints Class """

# Containers

class CollectionsPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Collections Endpoints Class """

    def collections_list_read(self, query_params=None):
        return self.execute_compute('GET', 'api/v1/collections', query_params=query_params, paginated=True)

    def collection_usages(self, collection_id):
        return self.execute_compute('GET', 'api/v1/collections/%s/usages' % collection_id, paginated=True)

    # Note: No response is returned upon successful execution of POST, PUT, and DELETE.
    # You must verify the collection via collections_list_read() or the Console.

    def collection_create(self, body_params):
        return self.execute_compute('POST', 'api/v1/collections', body_params=body_params)

    def collection_update(self, collection_id, body_params):
        return self.execute_compute('PUT', 'api/v1/collections/%s' % collection_id, body_params=body_params)

    def collection_delete(self, collection_id):
        return self.execute_compute('DELETE', 'api/v1/collections/%s' % collection_id)
