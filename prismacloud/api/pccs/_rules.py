""" Prisma Cloud Code Security API Enforcement Rules Endpoints Class """

# enforcement-rules

class RulesPrismaCloudAPIPCCSMixin:
    """ Prisma Cloud Code Security API Enforcement Rules Endpoints Class """

    def enforcement_rules_read(self):
        return self.execute_code_security('GET', 'code/api/v1/enforcement-rules')

    def enforcement_rules_update(self, rules):
        return self.execute_code_security('PUT', 'code/api/v1/enforcement-rules', body_params=rules)
    
    def enforcement_rules_exception_create(self, policy_id, rule):
        return self.execute_code_security('POST', 'code/api/v1/enforcement-rules', body_params=rule)

    def enforcement_rules_exception_delete(self, rule_id):
        return self.execute_code_security('DELETE', 'code/api/v1/enforcement-rules/%s' % (rule_id))
