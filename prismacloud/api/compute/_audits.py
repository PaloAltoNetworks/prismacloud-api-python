""" Prisma Cloud Compute API Containers Endpoints Class """

# Containers

class AuditsPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Audit Endpoints Class """

    # The audits/incidents endpoint is the only documented audits endpoint.
    # It maps to the table in Compute > Monitor > Runtime > Incident Explorer in the Console.
    # Reference: https://prisma.pan.dev/api/cloud/cwpp/audits

    def audits_list_read(self, audit_type='incidents', query_params=None):
        audits = self.execute_compute('GET', 'api/v1/audits/%s?' % audit_type, query_params=query_params, paginated=True)
        return audits

    def audits_ack_incident(self, incident_id, ack_status = True):
        body_params = {"acknowledged": ack_status}
        resp = self.execute_compute('PATCH', 'api/v1/audits/incidents/acknowledge/%s' % incident_id, body_params=body_params)
        return resp

    # Other related and undocumented endpoints.

    # Compute > Monitor > Events

    @staticmethod
    def compute_audit_types():
        return [
            # Containers
            'access',
            'admission',
            'firewall/app/app-embedded',
            'firewall/app/container',
            'kubernetes',
            'runtime/app-embedded',
            'runtime/container',
            'trust',
            # Hosts
            'firewall/app/host',
            'runtime/file-integrity',
            'runtime/host',
            'runtime/log-inspection',
            # Serverless
            'firewall/app/serverless',
            'runtime/serverless',
            # Incidents
            'incidents'
        ]

    # Hosts > Host Activities

    def host_forensic_activities_list_read(self, query_params=None):
        audits = self.execute_compute('GET', 'api/v1/forensic/activities?', query_params=query_params, paginated=True)
        return audits

    # Compute > Manage > History

    def console_history_list_read(self, query_params=None):
        logs = self.execute_compute('GET', 'api/v1/audits/mgmt?', query_params=query_params)
        return logs
