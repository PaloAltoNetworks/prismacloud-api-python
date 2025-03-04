""" Prisma Cloud Compute API Custom Feeds Endpoints Class """

# Custom Feeds (Manage > System)

class FeedsPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Custom Feeds Endpoints Class """

    # body_params = {"feed": ["10.10.10.10", "10.10.10.200"] }
    #
    def feeds_ips_write(self, body_params):
        return self.execute_compute('PUT', 'api/v1/feeds/custom/ips', body_params=body_params)

    # body_params = {
    #     "feed": [
    #         {
    #              "name":    "example",
    #              "md5":     "cdb55ac14abdf2b868a06f90e939fba6",
    #              "allowed": False
    #         },
    #         {
    #              "name":    "example_02",
    #              "md5":     "d3af4a715add78009b4483acb95e4c34",
    #              "allowed": False
    #         }
    #     ]
    # }
    #
    def feeds_malware_write(self, body_params):
        return self.execute_compute('PUT', 'api/v1/feeds/custom/malware', body_params=body_params)

    # body_params = {
    #     "_id": "",
    #     "modified": "2023-02-15T22:22:21.804Z",
    #     "feed": [
    #         {
    #             "name":    "example_malware",
    #             "md5":     "cdb55ac14abdf2b868a06f90e939fba6",
    #             "allowed": True
    #         }
    #     ],
    #     "digest": "0880945af4ab1be95aa073305526c811"
    # }
    #
    # def feeds_trusted_executables_write(self, body_params):
    #     return self.execute_compute('PUT', 'api/v1/feeds/custom/malware', body_params=body_params)

    # body_params = {
    #     "_id": "customVulnerabilities",
    #     "rules": [
    #         {
    #             "name":                "example_01",
    #             "type":                "package",
    #             "package":             "example_package_01",
    #             "minVersionInclusive": "1.0",
    #             "maxVersionInclusive": "2.0",
    #             "md5":                 ""
    #         },
    #         {
    #             "_id":                  "",
    #             "name":                 "example_02",
    #             "package":              "example_package_02",
    #             "type":                 "package",
    #             "minVersionInclusive": "2.0",
    #             "maxVersionInclusive": "3.0",
    #             "md5": ""
    #         }
    #     ],
    #     "digest": "e9c36ba88b22338d0f9b6f7fe4c0113d"
    # }
    #
    # def feeds_trusted_executables_write(self, body_params):
    #     return self.execute_compute('PUT', 'api/v1/feeds/custom/custom-vulnerabilities', body_params=body_params)

    # body_params = {"rules": [{"cve":"CVE-12345", "description":""}] }
    #
    # def feeds_cve_allow_list_write(self, body_params):
    #     return self.execute_compute('PUT', 'api/v1/feeds/custom/cve-allow-list', body_params=body_params)
