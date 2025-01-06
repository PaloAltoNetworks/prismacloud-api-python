"""Unit test for PrismaCloudAPICWPPMixin class
"""
import unittest
import json

import responses
from responses import registries, matchers
from prismacloud.api.pc_lib_api import PrismaCloudAPI
from tests.data import SETTINGS, META_INFO, CREDENTIALS, ONE_HOST


class TestCasePrismaCloudAPICWPPMixin(unittest.TestCase):
    """Unit test on execute_compute method
    """
    @responses.activate
    def setUp(self):
        """Setup the login and meta_info route to get a mock PrimaCloudAPI object used on test
        """
        responses.post(
            "https://example.prismacloud.io/login",
            body=json.dumps({"token": "token"}),
            status=200,
        )
        responses.get(
            "https://example.prismacloud.io/meta_info",
            body=json.dumps(META_INFO),
            status=200,
        )
        self.pc_api = PrismaCloudAPI()
        self.pc_api.configure(SETTINGS)

    @responses.activate
    def test_execute_compute_nominal_for_credentials_list(self):
        """Nominal test on the mock credentials list route
        """
        get_creds = responses.get(
            "https://example.prismacloud.io/api/v1/credentials",
            body=json.dumps(CREDENTIALS),
            status=200
        )
        crendtials_list = self.pc_api.execute_compute(
            'GET', 'api/v1/credentials')
        self.assertIsInstance(crendtials_list, list)
        self.assertEqual(len(crendtials_list), 1)
        self.assertEqual(get_creds.call_count, 1)

    @responses.activate
    def test_execute_compute_without_token_for_credentials_list(self):
        """Nominal test on the mock credentials list route with missing Prisma token
        On this case, we check the login phase
        """
        self.pc_api.token = None
        responses.post(
            "https://example.prismacloud.io/login",
            body=json.dumps({"token": "token"}),
            status=200
        )
        get_creds = responses.get(
            "https://example.prismacloud.io/api/v1/credentials",
            body=json.dumps(CREDENTIALS),
            status=200
        )
        crendtials_list = self.pc_api.execute_compute(
            'GET',
            'api/v1/credentials',
        )
        self.assertIsInstance(crendtials_list, list)
        self.assertEqual(len(crendtials_list), 1)
        self.assertEqual(get_creds.call_count, 1)

    @responses.activate
    def test_execute_compute_with_an_expire_token_for_credentials_list(self):
        """Nominal test on the mock credentials list route with an expired Prisma token
        On this case, we check the re-login phase
        """
        self.pc_api.token_timer = 0.0
        responses.post(
            "https://example.prismacloud.io/login",
            body=json.dumps({"token": "token"}),
            status=200
        )
        get_creds = responses.get(
            "https://example.prismacloud.io/api/v1/credentials",
            body=json.dumps(CREDENTIALS),
            status=200
        )
        crendtials_list = self.pc_api.execute_compute(
            'GET',
            'api/v1/credentials',
        )
        self.assertIsInstance(crendtials_list, list)
        self.assertEqual(len(crendtials_list), 1)
        self.assertEqual(get_creds.call_count, 1)

    @responses.activate(registry=registries.OrderedRegistry)
    def test_execute_compute_retry_for_credentials_list(self):
        """Nominal test on the mock credentials list route with an 500 error
        On the first call we send a 500 error before getting it 200 to test the retry mecanisme
        """
        get_creds_1 = responses.get(
            'https://example.prismacloud.io/api/v1/credentials',
            body=json.dumps({}),
            status=500,
        )
        get_creds_2 = responses.get(
            'https://example.prismacloud.io/api/v1/credentials',
            body=json.dumps(CREDENTIALS),
            status=200,
        )

        crendtials_list = self.pc_api.execute_compute(
            'GET',
            'api/v1/credentials',
        )
        self.assertIsInstance(crendtials_list, list)
        self.assertEqual(len(crendtials_list), 1)
        self.assertEqual(get_creds_1.call_count, 1)
        self.assertEqual(get_creds_2.call_count, 1)

    @responses.activate(registry=registries.OrderedRegistry)
    def test_execute_compute_retry_failed_for_credentials_list(self):
        """Non expected test on the mock credentials list route with multiple 500 error
        We setup for all call a 500 error return and test if the right exception is raise
        """
        self.pc_api.retry_number = 2
        get_creds_responses = [
            responses.get(
                'https://example.prismacloud.io/api/v1/credentials',
                body=json.dumps({}),
                status=500,
            )
            for _ in range(3)
        ]
        with self.assertRaises(SystemExit) as context:
            self.pc_api.execute_compute(
                'GET',
                'api/v1/credentials'
            )
        self.assertEqual(
            str(context.exception),
            """

Status Code: 500
API: (https://example.prismacloud.io/api/v1/credentials) with query params: (None) and body params: (None) responded with an error and this response:
{}

"""
        )
        for get_cred in get_creds_responses:
            self.assertEqual(get_cred.call_count, 1)

    @responses.activate(registry=registries.OrderedRegistry)
    def test_execute_compute_nominal_for_hosts_list(self):
        """Norminal test on the mock hosts list route
        We expected to get 52 hosts
        """
        get_host_1 = responses.get(
            "https://example.prismacloud.io/api/v1/hosts",
            body=json.dumps([json.dumps(ONE_HOST) for _ in range(0, 50)]),
            status=200,
            headers={"Total-Count": "52"}
        )
        get_host_2 = responses.get(
            "https://example.prismacloud.io/api/v1/hosts",
            body=json.dumps([json.dumps(ONE_HOST) for _ in range(0, 2)]),
            status=200,
            headers={"Total-Count": "52"}
        )
        hosts = self.pc_api.execute_compute(
            'GET',
            'api/v1/hosts',
            paginated=True,
        )
        self.assertEqual(len(hosts), 52)
        self.assertEqual(get_host_1.call_count, 1)
        self.assertEqual(get_host_2.call_count, 1)

    @responses.activate(registry=registries.OrderedRegistry)
    def test_execute_compute_failed_all_hosts_list_because_unexpected_status_code_using_force_parameter(self):
        """Non expected test on the mock hosts list route with a 404 HTTP error code
        The first batch of hosts is correctly send by the second batch have an expected error code
        Since the force flag is set, we expected a 50 hosts list and no raised exception
        """
        get_host_1 = responses.get(
            "https://example.prismacloud.io/api/v1/hosts",
            body=json.dumps([json.dumps(ONE_HOST) for _ in range(0, 50)]),
            status=200,
            headers={"Total-Count": "52"}
        )
        get_host_2 = responses.get(
            "https://example.prismacloud.io/api/v1/hosts",
            body=json.dumps([json.dumps(ONE_HOST) for _ in range(0, 2)]),
            status=404,
            headers={"Total-Count": "52"}
        )
        hosts = self.pc_api.execute_compute(
            'GET',
            'api/v1/hosts',
            paginated=True,
            force=True
        )
        self.assertEqual(len(hosts), 50)
        self.assertEqual(get_host_1.call_count, 1)
        self.assertEqual(get_host_2.call_count, 1)

    @responses.activate(registry=registries.OrderedRegistry)
    def test_execute_compute_failed_all_hosts_list_because_unexpected_status_code_without_force_parameter(self):
        """Non expected test on the mock hosts list route with a 404 HTTP error code
        The first batch of hosts is correctly send by the second batch have an expected error code
        We must have a raised exception and no host response
        """
        get_host_1 = responses.get(
            "https://example.prismacloud.io/api/v1/hosts",
            body=json.dumps([json.dumps(ONE_HOST) for _ in range(0, 50)]),
            status=200,
            headers={"Total-Count": "52"}
        )
        get_host_2 = responses.get(
            "https://example.prismacloud.io/api/v1/hosts",
            body=json.dumps({}),
            status=404,
            headers={"Total-Count": "52"}
        )
        with self.assertRaises(SystemExit) as context:
            self.pc_api.execute_compute(
                'GET',
                'api/v1/hosts',
                paginated=True
            )
        self.assertEqual(get_host_1.call_count, 1)
        self.assertEqual(get_host_2.call_count, 1)
        self.assertEqual(str(context.exception), """

Status Code: 404
API: (https://example.prismacloud.io/api/v1/hosts?limit=50&offset=50) with query params: (None) and body params: (None) responded with an error and this response:
{}

""")

    @responses.activate(registry=registries.OrderedRegistry)
    def test_excute_compute_nominal_for_tag_update(self):
        """Nominal test on the mock tags put
        We expect no response
        """
        put_tag = responses.put(
            "https://example.prismacloud.io/api/v1/tags/my_tag",
            status=200,
            match=[
                matchers.json_params_matcher({
                    "name": "tag_name",
                    "color": "#ff0000",
                    "description": "A super cool tag",
                })
            ]
        )
        response = self.pc_api.execute_compute(
            'PUT',
            'api/v1/tags/my_tag',
            body_params={
                "name": "tag_name",
                "color": "#ff0000",
                "description": "A super cool tag",
            },
        )
        self.assertIsNone(response)
        self.assertEqual(put_tag.call_count, 1)

    @responses.activate
    def test_execute_compute_failed_because_bad_status_code(self):
        """Non expected test on the mock credentials list route with an 404 error
        We expect an expection raised
        """
        get_creds = responses.get(
            "https://example.prismacloud.io/api/v1/credentials",
            body=json.dumps(CREDENTIALS),
            status=404
        )
        with self.assertRaises(SystemExit) as context:
            self.pc_api.execute_compute(
                'GET',
                'api/v1/credentials',
            )
        self.assertEqual(
            str(context.exception),
            f"""

Status Code: 404
API: (https://example.prismacloud.io/api/v1/credentials) with query params: (None) and body params: (None) responded with an error and this response:
{json.dumps(CREDENTIALS)}

"""
        )
        self.assertEqual(get_creds.call_count, 1)

    @responses.activate
    def test_execute_compute_with_csv_content_type(self):
        """Nominal test on the mock discovery cloud download file on CSV
        """
        discovery = responses.get(
            "https://example.prismacloud.io/api/v1/cloud/discovery/download",
            body="discovery_download",
            status=200,
            content_type="text/csv",
        )
        download = self.pc_api.execute_compute(
            "GET", "api/v1/cloud/discovery/download")
        self.assertEqual(discovery.call_count, 1)
        self.assertEqual(download, "discovery_download")
