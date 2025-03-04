## Adding Endpoints

While most of the endpoints documented in the [CSPM API Reference](https://prisma.pan.dev/api/cloud/cspm) are defined as methods in this SDK,
some are not, as endpoints are added to Prisma Cloud as features are added.

To add an method for an endpoint to `_endpoints.py`, refer to the above API Reference, and use the existing methods as examples.

---

class EndpointsPrismaCloudAPIMixin():
    """ Prisma Cloud API Endpoints Class """

    def example_list(self):
        return self.execute('GET', 'example/endpoint')