""" Prisma Cloud Code Security API Code Policies Endpoints Class """

# Code Policies

class CodePoliciesPrismaCloudAPIPCCSMixin:
    """ Prisma Cloud Code Security API Code Policies Endpoints Class """

    def code_policies_list_read(self, policy_id):
        return self.execute_code_security('GET', 'code/api/v2/policies/%s' % policy_id)
