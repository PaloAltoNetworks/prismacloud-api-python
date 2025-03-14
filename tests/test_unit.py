""" Unit Tests """

import unittest

from unittest import mock

# pylint: disable=import-error
from prismacloud.api import pc_api
from tests.data import META_INFO, SETTINGS, USER_PROFILE


class TestPrismaCloudAPI(unittest.TestCase):
    """ Unit Tests with Mocking """

    # Decorator
    @mock.patch('prismacloud.api.cspm.EndpointsPrismaCloudAPIMixin.meta_info')
    def test_pc_api_configure(self, meta_info):
        meta_info.return_value = META_INFO
        pc_api.configure(SETTINGS)
        self.assertEqual(pc_api.api_compute, 'example.prismacloud.io')

    # With
    def test_pc_api_current_user(self):
        with mock.patch('prismacloud.api.PrismaCloudAPI.execute') as pc_api_execute:
            pc_api_execute.return_value = USER_PROFILE
            result = pc_api.current_user()
            self.assertEqual(result['displayName'], 'Example User')
