class Images_PrismaCloudAPICompute_Mixin:

   # Images (Monitor > Vulnerabilities/Compliance > Images > Deployed)

    def images_list_read(self, image_id=None):
        if image_id:
            images = self.execute_compute('GET', 'api/v1/images?id=%s&filterBaseImage=true' % image_id)
        else:
            images = self.execute_compute('GET', 'api/v1/images?filterBaseImage=true', paginated=True)
        return images
