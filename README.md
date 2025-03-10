# Python SDK for the Prisma Cloud APIs

This is a Python SDK for the Prisma Cloud APIs (CSPM, CWPP, and PCCS) in the form of a Python package.

This package is a fork of [prismacloud-api-python](https://github.com/PaloAltoNetworks/prismacloud-api-python), package [prismacloud-api](https://pypi.org/project/prismacloud-api), forked at version 5.2.24.

This package is not maintained by Prisma Cloud SEs.

It also includes reference scripts that utilize this SDK.



## Table of Contents

* [Installation](#Installation)
* [Support](#Support)
* [References](#References)
* [Changelog](#Changelog)


## Installation

Install the SDK via `pip`:

```
pip3 install prismacloudapi
```

Please refer to [PyPI](https://pypi.org/project/prismacloudapi) for details.

### Example Scripts

Please refer to this [scripts](https://github.com/PaloAltoNetworks/prismacloud-api-python/tree/main/scripts) directory for configuration, documentation, and usage.

If you prefer to use this SDK without using command-line options, consider these minimal examples:

#### Prisma Cloud Enterprise Edition

```
import os
from prismacloud.api import pc_api

# Settings for Prisma Cloud Enterprise Edition

settings = {
    "url":      "https://api.prismacloud.io/",
    "identity": "access_key",
    "secret":   "secret_key"
}

pc_api.configure(settings)

print('Prisma Cloud API Current User:')
print()
print(pc_api.current_user())
print()
print('Prisma Cloud Compute API Intelligence:')
print()
print(pc_api.statuses_intelligence())
print()

print('Prisma Cloud API Object:')
print()
print(pc_api)
print()
```

#### Prisma Cloud Compute Edition

```
import os
from prismacloud.api import pc_api

# Settings for Prisma Cloud Compute Edition

settings = {
    "url":      "https://console.example.com/",
    "identity": "username",
    "secret":   "password"
}

pc_api.configure(settings)

print('Prisma Cloud Compute API Intelligence:')
print()
print(pc_api.statuses_intelligence())
print()

print('Prisma Cloud API Object:')
print()
print(pc_api)
print()
```

Settings can also be defined as environment variables:

#### Environment Variables

```
settings = {
    "url":      os.environ.get('PC_URL'),
    "identity": os.environ.get('PC_IDENTITY'),
    "secret":   os.environ.get('PC_SECRET')
}
```

## Support

This package is not maintained by Prisma Cloud SEs or any Palo Alto Networks employees.

The maintainers will make a best-effort to address issues, and (of course) contributors are encouraged to submit issues and pull requests.


## References

Prisma Cloud APIs:

https://prisma.pan.dev/api/cloud/

Access Keys:

https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin/manage-prisma-cloud-administrators/create-access-keys.html

Permissions:

https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin/manage-prisma-cloud-administrators/prisma-cloud-admin-permissions.html

## Changelog

2025-03 Major changes with Version 5.2.28:
* Leverage iterator construct for large dataset

2024-01 Major changes with Version 5.0:
* Command-line argument and configuration file changes.
