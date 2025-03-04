""" Unit Tests """

import unittest

import mock

# pylint: disable=import-error
from prismacloudapi import pc_api

class TestPrismaCloudAPI(unittest.TestCase):
    """ Unit Tests with Mocking """

    SETTINGS = {
            'name':     'Example Tenant',
            'identity': 'abc',
            'secret':   'def',
            'url':      'example.prismacloud.io',
            'verify':   False,
            'debug':    False
    }

    USER_PROFILE = {
        'email': 'example@example.com',
        'firstName': 'Example',
        'lastName': 'User',
        'timeZone': 'America/Los_Angeles',
        'enabled': True,
        'lastModifiedBy': 'template@redlock.io',
        'lastModifiedTs': 1630000000000,
        'lastLoginTs': 1640000000000,
        'displayName': 'Example User',
        'accessKeysAllowed': True,
        'defaultRoleId': '1234-5678',
        'roleIds': ['1234-5678'],
        'roles': [{
            'id': '1234-5678',
            'name': 'System Admin',
            'type': 'System Admin',
            'onlyAllowCIAccess': False,
            'onlyAllowComputeAccess': False,
            'onlyAllowReadAccess': False
        }],
        'activeRole': {
            'id': '1234-5678',
            'name': 'System Admin',
            'type': 'System Admin',
            'onlyAllowCIAccess': False,
            'onlyAllowComputeAccess': False,
            'onlyAllowReadAccess': False
        }
    }

    # Decorator
    @mock.patch('prismacloudapi.pc_utility.get_settings')
    def test_pc_api_configure(self, get_settings):
        get_settings.return_value = self.SETTINGS
        settings = get_settings()
        pc_api.configure(settings)
        self.assertEqual('example.prismacloud.io', pc_api.url)

    # With
    def test_pc_api_current_user(self):
        with mock.patch('prismacloudapi.PrismaCloudAPI.execute') as pc_api_execute:
            pc_api_execute.return_value = self.USER_PROFILE
            result = pc_api.current_user()
            self.assertEqual('Example User', result['displayName'])

if __name__ == '__main__':
    unittest.main()
