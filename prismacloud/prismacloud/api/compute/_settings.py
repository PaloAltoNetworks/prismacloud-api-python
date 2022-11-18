""" Prisma Cloud Compute API Settings Endpoints Class """

# Credentials (Defend > Compliance)

class SettingsPrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Settings Endpoints Class """

    def settings_serverless_scan_read(self):
        return self.execute_compute('get', 'api/v1/settings/serverless-scan')

    def settings_serverless_scan_write(self, body):
        return self.execute_compute(
            'put', 'api/v1/settings/serverless-scan',
            body_params=body
        )

    def settings_registry_read(self):
        return self.execute_compute('get', 'api/v1/settings/registry')

    def settings_registry_write(self, body):
        return self.execute_compute(
            'put', 'api/v1/settings/registry',
            body_params=body
        )

    def settings_host_auto_deploy_read(self):
        return self.execute_compute('get', 'api/v1/settings/host-auto-deploy')

    def settings_host_auto_deploy_write(self, body):
        return self.execute_compute(
            'post', 'api/v1/settings/host-auto-deploy',
            body_params=body
        )
