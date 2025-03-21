""" Prisma Compute API Cloud Endpoints Class """


# Cloud

class CloudPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Cloud Endpoints Class """

    def cloud_discovery_read(self, sort=None, reverse=None,
                             provider=None, credential_id=None, service_type=None, registry=None, account_name=None,
                             agentless=None, zone=None,
                             ):
        """
        Returns a list of all cloud discovery scan results in a paginated response.
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cwpp/get-cloud-discovery/>`_
        """
        query_params = dict(sort=sort, reverse=reverse,
                            provider=provider, credentialID=credential_id, serviceType=service_type, registry=registry,
                            accountName=account_name, agentless=agentless,
                            zone=zone,
                            )
        for k, v in dict(query_params).items():
            if v is None:
                del query_params[k]
            elif isinstance(v, list):
                query_params[k] = ','.join(v)
        return self.execute_compute_paginated('GET', 'api/v1/cloud/discovery', query_params=query_params)

    def cloud_discovery_download(self, query_params=None):
        # request_headers = {'Content-Type': 'text/csv'}
        # return self.execute_compute('GET', 'api/v1/cloud/discovery/download?', request_headers=request_headers, query_params=query_params)
        return self.execute_compute('GET', 'api/v1/cloud/discovery/download', query_params=query_params)

    def cloud_discovery_scan(self):
        return self.execute_compute('POST', 'api/v1/cloud/discovery/scan')

    def cloud_discovery_scan_stop(self):
        return self.execute_compute('POST', 'api/v1/cloud/discovery/stop')

    def cloud_discovery_vms(self, query_params=None):
        return self.execute_compute_paginated('GET', 'api/v1/cloud/discovery/vms', query_params=query_params)

    def cloud_discovery_entities(self, query_params=None):
        return self.execute_compute_paginated('GET', 'api/v1/cloud/discovery/entities', query_params=query_params)

    def cloud_discovery_entities2(self, sort=None, reverse=None, credential_id=None, service_type=None, registry=None,
                                  zone=None, defended=None, images=None,
                                  ):
        """
        Returns a list of discovered cloud entities.
        `PAN Api docs <https://pan.dev/prisma-cloud/api/cwpp/get-cloud-discovery-entities/>`_
        """
        query_params = dict(
            sort=sort, reverse=reverse,
            credentialID=credential_id, serviceType=service_type, registry=registry,
            zone=zone,
            defended=defended, images=images
        )
        for k, v in dict(query_params).items():
            if v is None:
                del query_params[k]
            elif isinstance(v, list):
                query_params[k] = ','.join(v)
        return self.execute_compute_paginated('GET', 'api/v1/cloud/discovery/entities', query_params=query_params)
