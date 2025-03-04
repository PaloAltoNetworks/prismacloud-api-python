## Adding Endpoints

While most of the endpoints documented in the [CWP API Reference](https://prisma.pan.dev/api/cloud/cwpp) are defined as methods in this SDK,
some are not, as endpoints are added to Prisma Cloud as features are added.

To add an method for an endpoint, refer to the above API Reference, and use the existing methods as examples.

Each logical set of endpoints (defined by URL prefix) is grouped into its own file, and imported in `__init__.py `.

When adding a new group of endpoints, create a new file, and import it using the existing imports as examples.

---

In `__init__.py `:

```
from ._example.py import *
```

In `_example.py`:

```
""" Prisma Cloud Compute API Example Endpoints Class """

class ExamplePrismaCloudAPIComputeMixin:
    """ Prisma Cloud Compute API Example Endpoints Class """

    def example_list(self):
        return self.execute_compute('GET', '/api/v1/example/endpoint')
```