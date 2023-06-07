""" Prisma Cloud Compute API VMs Endpoints Class """

# Containers


class VMsPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API VMs Endpoints Class """

    # VM Image table in Monitor > Vulnerabilities > Hosts > VMs
    def vms_list_read(self, query_params=None):
        vms = self.execute_compute(
            'GET', 'api/v1/vms', query_params=query_params, paginated=True)
        return vms