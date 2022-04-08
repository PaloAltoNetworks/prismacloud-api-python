""" Unit Tests """

import unittest

import mock

# pylint: disable=import-error
from prismacloud.api import pc_api

class TestPrismaCloudAPI(unittest.TestCase):
    """ Unit Tests with Mocking """

    SETTINGS = {
            'username':    'abc',
            'password':    'def',
            'api':         'example.prismacloud.io',
            'api_compute': 'prismacloud.example.com',
            'ca_bundle':   False,
            'debug':       False
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
    @mock.patch('prismacloud.api.pc_utility.get_settings')
    def test_pc_api_configure(self, get_settings):
        get_settings.return_value = self.SETTINGS
        settings = get_settings()
        pc_api.configure(settings)
        self.assertEqual('example.prismacloud.io', pc_api.api)

    # With
    def test_pc_api_current_user(self):
        with mock.patch('prismacloud.api.PrismaCloudAPI.execute') as pc_api_execute:
            pc_api_execute.return_value = self.USER_PROFILE
            result = pc_api.current_user()
            self.assertEqual('Example User', result['displayName'])

if __name__ == '__main__':
    unittest.main()
