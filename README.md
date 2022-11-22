# Python SDK for the Prisma Cloud APIs

This project includes a Python SDK for the Prisma Cloud APIs (CSPM, CWPP, and CCS) in the form of a Python package.
It also includes reference scripts that utilize this SDK.

Major changes with Version 5.0:

* Command-line argument and configuration file changes.

## Table of Contents

* [Setup](#Setup)
* [Support](#Support)


## Setup

Install the SDK via `pip3`:

```
pip3 install prismacloud-api
```

Please refer to [PyPI](https://pypi.org/project/prismacloud-api) for details.

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

This project has been developed by members of the Prisma Cloud CS and SE teams, it is not Supported by Palo Alto Networks.
Nevertheless, the maintainers will make a best-effort to address issues, and (of course) contributors are encouraged to submit issues and pull requests.
