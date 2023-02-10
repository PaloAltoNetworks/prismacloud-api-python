""" Prisma Cloud Compute API Audits Endpoints Class """

class AuditsPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Audit Endpoints Class """

    # The audits/incidents endpoint is the only documented audits endpoint.
    # It maps to the table in Compute > Monitor > Runtime > Incident Explorer in the Console.
    # Reference: https://prisma.pan.dev/api/cloud/cwpp/audits

    def audits_list_read(self, audit_type='incidents', query_params=None):
        audits = self.execute_compute('GET', 'api/v1/audits/%s' % audit_type, query_params=query_params, paginated=True)
        return audits

    # Other related and undocumented endpoints.

    # Forensics (Here in audits, as this endpoint is also undocumented like audits.)

    def forensic_read(self, workload_id, workload_type, defender_hostname):
        query_params = {'hostname': defender_hostname}
        if workload_type in ['container', 'app-embedded']:
            response = self.execute_compute('GET', 'api/v1/profiles/%s/%s/forensic/bundle' % (workload_type, workload_id), query_params=query_params)
        elif workload_type == 'host':
            response = self.execute_compute('GET', 'api/v1/profiles/%s/%s/forensic/download' % (workload_type, workload_id), query_params=query_params)
        else:
            response = self.execute_compute('GET', 'api/v1/profiles/%s/%s/forensic' % (workload_type, workload_id), query_params=query_params, paginated=True)
        return response

    # Monitor / Runtime > Incident Explorer

    def audits_ack_incident(self, incident_id, ack_status=True):
        body_params = {'acknowledged': ack_status}
        response = self.execute_compute('PATCH', 'api/v1/audits/incidents/acknowledge/%s' % incident_id, body_params=body_params)
        return response

    # Compute > Monitor > Events

    @staticmethod
    def compute_audit_types():
        return [
            # Containers
            'access',
            'admission',
            'firewall/app/app-embedded',
            'firewall/app/app-embedded',
            'firewall/network/container',
            'kubernetes',
            'runtime/app-embedded',
            'runtime/container',
            'trust',
            # Hosts
            'firewall/app/host',
            'firewall/network/host',
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
        audits = self.execute_compute('GET', 'api/v1/forensic/activities', query_params=query_params, paginated=True)
        return audits

    # Compute > Manage > History

    def console_history_list_read(self, query_params=None):
        logs = self.execute_compute('GET', 'api/v1/audits/mgmt', query_params=query_params)
        return logs
