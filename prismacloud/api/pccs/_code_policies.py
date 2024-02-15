""" Prisma Cloud Code Security API Code Policies Endpoints Class """

# Code Policies

class CodePoliciesPrismaCloudAPIPCCSMixin:
    """ Prisma Cloud Code Security API Code Policies Endpoints Class """
    
    def code_policies_list_read(self, policy_id=None):
        if policy_id:
            # Fetch details for a specific policy
            return self.execute_code_security('GET', 'code/api/v2/policies/%s' % policy_id)
        else:
            # Fetch a list of all policies if no specific policy_id is provided
            return self.execute_code_security('GET', 'code/api/v2/policies')
