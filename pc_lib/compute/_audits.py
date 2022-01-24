""" Prisma Cloud Compute API Containers Endpoints Class """

# Containers

class AuditsPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Audit Endpoints Class """

    # The audits/incidents endpoint is the only documented audits endpoint.
    # It maps to the table in Compute > Monitor > Runtime > Incident Explorer in the Console.
    # Reference: https://prisma.pan.dev/api/cloud/cwpp/audits

    def audits_list_read(self, audit_type='incidents', query_params=None):
        audits = self.execute_compute('GET', 'api/v1/audits/%s' % audit_type, query_params=query_params, paginated=True)
        return audits

    """
    Other Audits Endpoints

    Compute > Monitor > Events ...

    Containers:

    api/v1/audits/runtime/container
    api/v1/audits/firewall/app/container
    api/v1/audits/trust
    api/v1/audits/kubernetes
    api/v1/audits/admission
    api/v1/audits/access
    api/v1/audits/runtime/app-embedded
    api/v1/audits/firewall/app/app-embedded

    Hosts:

    api/v1/audits/runtime/host
    api/v1/audits/firewall/app/host
    api/v1/audits/runtime/log-inspection
    api/v1/audits/runtime/file-integrity
    api/v1/audits/forensic/activities

    Serverless:

    api/v1/audits/runtime/serverless
    api/v1/audits/firewall/app/serverless

    Compute > Manage > Logs ...

    History:

    api/v1/audits/mgmt

    Console (different, related endpoint):

    api/v1/logs/console


    Example query parameters ...

    aggregate=true
    fields=imageName,namespace,cluster,msg,time
    from=2022-01-01T12:34:56.789Z
    to=2022-01-31T012:34:56.789Z
    project=Example
    reverse=true
    sort=time
    """