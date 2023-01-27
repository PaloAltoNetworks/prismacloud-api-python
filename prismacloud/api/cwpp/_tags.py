""" Prisma Cloud Compute API Tags Endpoints Class """

# Tags are predefined labels that help you manage your vulnerabilities via the Console UI and Prisma Cloud Compute API.

class TagsPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Tags Endpoints Class """

    def tags_list_read(self):
        tags = self.execute_compute('GET', 'api/v1/tags')
        return tags

    def tag_add(self, body_params=None):
        result = self.execute_compute('POST', 'api/v1/tags', body_params=body_params)
        return result

    def tag_delete(self, tag_id):
        result = self.execute_compute('DELETE', 'api/v1/tags/%s' % tag_id)
        return result

    def tag_update(self, tag_id, body_params):
        result = self.execute_compute('PUT', 'api/v1/tags/%s' % tag_id, body_params=body_params)
        return result

    def tag_delete_vulnerability(self, tag_id, body_params):
        result = self.execute_compute('PUT', 'api/v1/tags/%s/vuln' % tag_id, body_params=body_params)
        return result

    def tag_set_vulnerability(self, tag_id, body_params):
        result = self.execute_compute('POST', 'api/v1/tags/%s/vuln' % tag_id, body_params=body_params)
        return result
