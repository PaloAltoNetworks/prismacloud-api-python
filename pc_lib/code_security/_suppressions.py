""" Prisma Cloud Code Security Suppressions Endpoints Class """

# Suppressions

class SuppressionsPrismaCloudAPICodeSecurityMixin:
    """ Prisma Cloud Code Security API Suppressions Endpoints Class """

    def suppressions_list_read(self):
        return self.execute_code_security('GET', 'code/api/v1/suppressions')

    def suppressions_create(self, policy_id, rule):
        return self.execute_code_security('POST', 'code/api/v1/suppressions/%s' % policy_id, body_params=rule)

    def suppressions_update(self, policy_id, rule_id, rule):
        return self.execute_code_security('PUT', 'code/api/v1/suppressions/%s/justifications/%s' % (policy_id, rule_id), body_params=rule)

    def suppressions_delete(self, policy_id, rule_id):
        return self.execute_code_security('DELETE', 'code/api/v1/suppressions/%s/justifications/%s' % (policy_id, rule_id))

    def suppressions_justifications_list_read(self, policy_id):
        return self.execute_code_security('GET', 'code/api/v1/suppressions/%s/justifications' % policy_id)
