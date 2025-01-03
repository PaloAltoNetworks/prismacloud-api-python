
SETTINGS = {
    'name':     'Example Tenant',
    'identity': 'abc',
    'secret':   'def',
    'url':      'example.prismacloud.io',
    'verify':   False,
    'debug':    False
}

META_INFO = {
    'twistlockUrl': 'example.prismacloud.io'
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

CREDENTIALS = [
    {
        "_id": "string",
        "accountGUID": "string",
        "accountID": "string",
        "accountName": "string",
        "apiToken": {
            "encrypted": "string",
            "plain": "string"
        },
        "azureSPInfo": {
            "clientId": "string",
            "miType": [
                "user-assigned",
                "system-assigned"
            ],
            "subscriptionId": "string",
            "tenantId": "string"
        },
        "caCert": "string",
        "cloudProviderAccountID": "string",
        "created": "2024-07-29T15:51:28.071Z",
        "description": "string",
        "external": True,
        "global": True,
        "lastModified": "2024-07-29T15:51:28.071Z",
        "ociCred": {
            "fingerprint": "string",
            "tenancyId": "string"
        },
        "owner": "string",
        "prismaLastModified": 0,
        "roleArn": "string",
        "secret": {
            "encrypted": "string",
            "plain": "string"
        },
        "skipVerify": True,
        "stsEndpoints": [
            "string"
        ],
        "tokens": {
            "awsAccessKeyId": "string",
            "awsSecretAccessKey": {
                "encrypted": "string",
                "plain": "string"
            },
            "duration": 0,
            "expirationTime": "2024-07-29T15:51:28.071Z",
            "token": {
                "encrypted": "string",
                "plain": "string"
            }
        },
        "type": [
            "aws",
            "azure",
            "gcp",
            "ibmCloud",
            "oci",
            "apiToken",
            "basic",
            "dtr",
            "kubeconfig",
            "certificate",
            "gitlabToken"
        ],
        "url": "string",
        "useAWSRole": True,
        "useSTSRegionalEndpoint": True
    }
]

ONE_HOST = {
    "Secrets": [
        "string"
    ],
    "_id": "string",
    "agentless": True,
    "aisUUID": "string",
    "allCompliance": {
        "compliance": [
            {
                "applicableRules": [
                    "string"
                ],
                "binaryPkgs": [
                    "string"
                ],
                "block": True,
                "cause": "string",
                "cri": True,
                "custom": True,
                "cve": "string",
                "cvss": 0,
                "description": "string",
                "discovered": "2024-07-29T15:51:28.071Z",
                "exploit": [
                    "",
                    "exploit-db",
                    "exploit-windows",
                    "cisa-kev"
                ],
                "exploits": [
                    {
                        "kind": [
                            "poc",
                            "in-the-wild"
                        ],
                        "link": "string",
                        "source": [
                            "",
                            "exploit-db",
                            "exploit-windows",
                            "cisa-kev"
                        ]
                    }
                ],
                "fixDate": 0,
                "fixLink": "string",
                "functionLayer": "string",
                "gracePeriodDays": 0,
                "id": 0,
                "layerTime": 0,
                "link": "string",
                "packageName": "string",
                "packageType": [
                    "nodejs",
                    "gem",
                    "python",
                    "jar",
                    "package",
                    "windows",
                    "binary",
                    "nuget",
                    "go",
                    "app",
                    "unknown"
                ],
                "packageVersion": "string",
                "published": 0,
                "riskFactors": {},
                "secret": {
                    "group": "string",
                    "locationInFile": "string",
                    "metadataModifiedTime": 0,
                    "modifiedTime": 0,
                    "originalFileLocation": "string",
                    "path": "string",
                    "permissions": "string",
                    "secretID": "string",
                    "size": 0,
                    "snippet": "string",
                    "type": [
                        "AWS Access Key ID",
                        "AWS Secret Key",
                        "AWS MWS Auth Token",
                        "Azure Storage Account Access Key",
                        "Azure Service Principal",
                        "GCP Service Account Auth Key",
                        "Private Encryption Key",
                        "Public Encryption Key",
                        "PEM X509 Certificate Header",
                        "SSH Authorized Keys",
                        "Artifactory API Token",
                        "Artifactory Password",
                        "Basic Auth Credentials",
                        "Mailchimp Access Key",
                        "NPM Token",
                        "Slack Token",
                        "Slack Webhook",
                        "Square OAuth Secret",
                        "Notion Integration Token",
                        "Airtable API Key",
                        "Atlassian Oauth2 Keys",
                        "CircleCI Personal Token",
                        "Databricks Authentication Token",
                        "GitHub Token",
                        "GitLab Token",
                        "Google API key",
                        "Grafana Token",
                        "Python Package Index Key (PYPI)",
                        "Typeform API Token",
                        "Scalr Token",
                        "Braintree Access Token",
                        "Braintree Payments Key",
                        "Paypal Token Key",
                        "Braintree Payments ID",
                        "Datadog Client Token",
                        "ClickUp Personal API Token",
                        "OpenAI API Key",
                        "Java DB Connectivity (JDBC)",
                        "MongoDB",
                        ".Net SQL Server"
                    ],
                    "user": "string"
                },
                "severity": "string",
                "status": "string",
                "templates": [
                    [
                        "PCI",
                        "HIPAA",
                        "NIST SP 800-190",
                        "GDPR",
                        "DISA STIG"
                    ]
                ],
                "text": "string",
                "title": "string",
                "twistlock": True,
                "type": [
                    "container",
                    "image",
                    "host_config",
                    "daemon_config",
                    "daemon_config_files",
                    "security_operations",
                    "k8s_master",
                    "k8s_worker",
                    "k8s_federation",
                    "linux",
                    "windows",
                    "istio",
                    "serverless",
                    "custom",
                    "docker_stig",
                    "openshift_master",
                    "openshift_worker",
                    "application_control_linux",
                    "gke_worker",
                    "image_malware",
                    "host_malware",
                    "aks_worker",
                    "eks_worker",
                    "image_secret",
                    "host_secret"
                ],
                "vecStr": "string",
                "vulnTagInfos": [
                    {
                        "color": "string",
                        "comment": "string",
                        "name": "string"
                    }
                ],
                "wildfireMalware": {
                    "md5": "string",
                    "path": "string",
                    "verdict": "string"
                }
            }
        ],
        "enabled": True
    },
    "appEmbedded": True,
    "applications": [
        {
            "installedFromPackage": True,
            "knownVulnerabilities": 0,
            "layerTime": 0,
            "name": "string",
            "originPackageName": "string",
            "path": "string",
            "service": True,
            "version": "string"
        }
    ],
    "baseImage": "string",
    "binaries": [
        {
            "altered": True,
            "cveCount": 0,
            "deps": [
                "string"
            ],
            "fileMode": 0,
            "functionLayer": "string",
            "md5": "string",
            "missingPkg": True,
            "name": "string",
            "path": "string",
            "pkgRootDir": "string",
            "services": [
                "string"
            ],
            "version": "string"
        }
    ],
    "cloudMetadata": {
        "accountID": "string",
        "awsExecutionEnv": "string",
        "image": "string",
        "labels": [
            {
                "key": "string",
                "sourceName": "string",
                "sourceType": [
                    "namespace",
                    "deployment",
                    "aws",
                    "azure",
                    "gcp",
                    "oci"
                ],
                "timestamp": "2024-07-29T15:51:28.071Z",
                "value": "string"
            }
        ],
        "name": "string",
        "provider": [
            "aws",
            "azure",
            "gcp",
            "alibaba",
            "oci",
            "others"
        ],
        "region": "string",
        "resourceID": "string",
        "resourceURL": "string",
        "type": "string",
        "vmID": "string",
        "vmImageID": "string"
    },
    "clusterType": [
        "AKS",
        "ECS",
        "EKS",
        "GKE",
        "Kubernetes"
    ],
    "clusters": [
        "string"
    ],
    "collections": [
        "string"
    ],
    "complianceDistribution": {
        "critical": 0,
        "high": 0,
        "low": 0,
        "medium": 0,
        "total": 0
    },
    "complianceIssues": [
        {
            "applicableRules": [
                "string"
            ],
            "binaryPkgs": [
                "string"
            ],
            "block": True,
            "cause": "string",
            "cri": True,
            "custom": True,
            "cve": "string",
            "cvss": 0,
            "description": "string",
            "discovered": "2024-07-29T15:51:28.071Z",
            "exploit": [
                "",
                "exploit-db",
                "exploit-windows",
                "cisa-kev"
            ],
            "exploits": [
                {
                    "kind": [
                        "poc",
                        "in-the-wild"
                    ],
                    "link": "string",
                    "source": [
                        "",
                        "exploit-db",
                        "exploit-windows",
                        "cisa-kev"
                    ]
                }
            ],
            "fixDate": 0,
            "fixLink": "string",
            "functionLayer": "string",
            "gracePeriodDays": 0,
            "id": 0,
            "layerTime": 0,
            "link": "string",
            "packageName": "string",
            "packageType": [
                "nodejs",
                "gem",
                "python",
                "jar",
                "package",
                "windows",
                "binary",
                "nuget",
                "go",
                "app",
                "unknown"
            ],
            "packageVersion": "string",
            "published": 0,
            "riskFactors": {},
            "secret": {
                "group": "string",
                "locationInFile": "string",
                "metadataModifiedTime": 0,
                "modifiedTime": 0,
                "originalFileLocation": "string",
                "path": "string",
                "permissions": "string",
                "secretID": "string",
                "size": 0,
                "snippet": "string",
                "type": [
                    "AWS Access Key ID",
                    "AWS Secret Key",
                    "AWS MWS Auth Token",
                    "Azure Storage Account Access Key",
                    "Azure Service Principal",
                    "GCP Service Account Auth Key",
                    "Private Encryption Key",
                    "Public Encryption Key",
                    "PEM X509 Certificate Header",
                    "SSH Authorized Keys",
                    "Artifactory API Token",
                    "Artifactory Password",
                    "Basic Auth Credentials",
                    "Mailchimp Access Key",
                    "NPM Token",
                    "Slack Token",
                    "Slack Webhook",
                    "Square OAuth Secret",
                    "Notion Integration Token",
                    "Airtable API Key",
                    "Atlassian Oauth2 Keys",
                    "CircleCI Personal Token",
                    "Databricks Authentication Token",
                    "GitHub Token",
                    "GitLab Token",
                    "Google API key",
                    "Grafana Token",
                    "Python Package Index Key (PYPI)",
                    "Typeform API Token",
                    "Scalr Token",
                    "Braintree Access Token",
                    "Braintree Payments Key",
                    "Paypal Token Key",
                    "Braintree Payments ID",
                    "Datadog Client Token",
                    "ClickUp Personal API Token",
                    "OpenAI API Key",
                    "Java DB Connectivity (JDBC)",
                    "MongoDB",
                    ".Net SQL Server"
                ],
                "user": "string"
            },
            "severity": "string",
            "status": "string",
            "templates": [
                [
                    "PCI",
                    "HIPAA",
                    "NIST SP 800-190",
                    "GDPR",
                    "DISA STIG"
                ]
            ],
            "text": "string",
            "title": "string",
            "twistlock": True,
            "type": [
                "container",
                "image",
                "host_config",
                "daemon_config",
                "daemon_config_files",
                "security_operations",
                "k8s_master",
                "k8s_worker",
                "k8s_federation",
                "linux",
                "windows",
                "istio",
                "serverless",
                "custom",
                "docker_stig",
                "openshift_master",
                "openshift_worker",
                "application_control_linux",
                "gke_worker",
                "image_malware",
                "host_malware",
                "aks_worker",
                "eks_worker",
                "image_secret",
                "host_secret"
            ],
            "vecStr": "string",
            "vulnTagInfos": [
                {
                    "color": "string",
                    "comment": "string",
                    "name": "string"
                }
            ],
            "wildfireMalware": {
                "md5": "string",
                "path": "string",
                "verdict": "string"
            }
        }
    ],
    "complianceIssuesCount": 0,
    "complianceRiskScore": 0,
    "compressed": True,
    "compressedLayerTimes": {
        "appTimes": [
            0
        ],
        "pkgsTimes": [
            {
                "pkgTimes": [
                    0
                ],
                "pkgsType": [
                    "nodejs",
                    "gem",
                    "python",
                    "jar",
                    "package",
                    "windows",
                    "binary",
                    "nuget",
                    "go",
                    "app",
                    "unknown"
                ]
            }
        ]
    },
    "creationTime": "2024-07-29T15:51:28.071Z",
    "csa": True,
    "csaWindows": True,
    "distro": "string",
    "ecsClusterName": "string",
    "err": "string",
    "errCode": 0,
    "externalLabels": [
        {
            "key": "string",
            "sourceName": "string",
            "sourceType": [
                "namespace",
                "deployment",
                "aws",
                "azure",
                "gcp",
                "oci"
            ],
            "timestamp": "2024-07-29T15:51:28.071Z",
            "value": "string"
        }
    ],
    "files": [
        {
            "md5": "string",
            "original_file_location": "string",
            "path": "string",
            "sha1": "string",
            "sha256": "string"
        }
    ],
    "firewallProtection": {
        "enabled": True,
        "outOfBandMode": [
            "",
            "Observation",
            "Protection"
        ],
        "ports": [
            0
        ],
        "supported": True,
        "tlsPorts": [
            0
        ],
        "unprotectedProcesses": [
            {
                "port": 0,
                "process": "string",
                "tls": True
            }
        ]
    },
    "firstScanTime": "2024-07-29T15:51:28.071Z",
    "foundSecrets": [
        {
            "group": "string",
            "locationInFile": "string",
            "metadataModifiedTime": 0,
            "modifiedTime": 0,
            "originalFileLocation": "string",
            "path": "string",
            "permissions": "string",
            "secretID": "string",
            "size": 0,
            "snippet": "string",
            "type": [
                "AWS Access Key ID",
                "AWS Secret Key",
                "AWS MWS Auth Token",
                "Azure Storage Account Access Key",
                "Azure Service Principal",
                "GCP Service Account Auth Key",
                "Private Encryption Key",
                "Public Encryption Key",
                "PEM X509 Certificate Header",
                "SSH Authorized Keys",
                "Artifactory API Token",
                "Artifactory Password",
                "Basic Auth Credentials",
                "Mailchimp Access Key",
                "NPM Token",
                "Slack Token",
                "Slack Webhook",
                "Square OAuth Secret",
                "Notion Integration Token",
                "Airtable API Key",
                "Atlassian Oauth2 Keys",
                "CircleCI Personal Token",
                "Databricks Authentication Token",
                "GitHub Token",
                "GitLab Token",
                "Google API key",
                "Grafana Token",
                "Python Package Index Key (PYPI)",
                "Typeform API Token",
                "Scalr Token",
                "Braintree Access Token",
                "Braintree Payments Key",
                "Paypal Token Key",
                "Braintree Payments ID",
                "Datadog Client Token",
                "ClickUp Personal API Token",
                "OpenAI API Key",
                "Java DB Connectivity (JDBC)",
                "MongoDB",
                ".Net SQL Server"
            ],
            "user": "string"
        }
    ],
    "history": [
        {
            "baseLayer": True,
            "created": 0,
            "emptyLayer": True,
            "id": "string",
            "instruction": "string",
            "sizeBytes": 0,
            "tags": [
                "string"
            ],
            "vulnerabilities": [
                {
                    "applicableRules": [
                        "string"
                    ],
                    "binaryPkgs": [
                        "string"
                    ],
                    "block": True,
                    "cause": "string",
                    "cri": True,
                    "custom": True,
                    "cve": "string",
                    "cvss": 0,
                    "description": "string",
                    "discovered": "2024-07-29T15:51:28.071Z",
                    "exploit": [
                        "",
                        "exploit-db",
                        "exploit-windows",
                        "cisa-kev"
                    ],
                    "exploits": [
                        {
                            "kind": [
                                "poc",
                                "in-the-wild"
                            ],
                            "link": "string",
                            "source": [
                                "",
                                "exploit-db",
                                "exploit-windows",
                                "cisa-kev"
                            ]
                        }
                    ],
                    "fixDate": 0,
                    "fixLink": "string",
                    "functionLayer": "string",
                    "gracePeriodDays": 0,
                    "id": 0,
                    "layerTime": 0,
                    "link": "string",
                    "packageName": "string",
                    "packageType": [
                        "nodejs",
                        "gem",
                        "python",
                        "jar",
                        "package",
                        "windows",
                        "binary",
                        "nuget",
                        "go",
                        "app",
                        "unknown"
                    ],
                    "packageVersion": "string",
                    "published": 0,
                    "riskFactors": {},
                    "secret": {
                        "group": "string",
                        "locationInFile": "string",
                        "metadataModifiedTime": 0,
                        "modifiedTime": 0,
                        "originalFileLocation": "string",
                        "path": "string",
                        "permissions": "string",
                        "secretID": "string",
                        "size": 0,
                        "snippet": "string",
                        "type": [
                            "AWS Access Key ID",
                            "AWS Secret Key",
                            "AWS MWS Auth Token",
                            "Azure Storage Account Access Key",
                            "Azure Service Principal",
                            "GCP Service Account Auth Key",
                            "Private Encryption Key",
                            "Public Encryption Key",
                            "PEM X509 Certificate Header",
                            "SSH Authorized Keys",
                            "Artifactory API Token",
                            "Artifactory Password",
                            "Basic Auth Credentials",
                            "Mailchimp Access Key",
                            "NPM Token",
                            "Slack Token",
                            "Slack Webhook",
                            "Square OAuth Secret",
                            "Notion Integration Token",
                            "Airtable API Key",
                            "Atlassian Oauth2 Keys",
                            "CircleCI Personal Token",
                            "Databricks Authentication Token",
                            "GitHub Token",
                            "GitLab Token",
                            "Google API key",
                            "Grafana Token",
                            "Python Package Index Key (PYPI)",
                            "Typeform API Token",
                            "Scalr Token",
                            "Braintree Access Token",
                            "Braintree Payments Key",
                            "Paypal Token Key",
                            "Braintree Payments ID",
                            "Datadog Client Token",
                            "ClickUp Personal API Token",
                            "OpenAI API Key",
                            "Java DB Connectivity (JDBC)",
                            "MongoDB",
                            ".Net SQL Server"
                        ],
                        "user": "string"
                    },
                    "severity": "string",
                    "status": "string",
                    "templates": [
                        [
                            "PCI",
                            "HIPAA",
                            "NIST SP 800-190",
                            "GDPR",
                            "DISA STIG"
                        ]
                    ],
                    "text": "string",
                    "title": "string",
                    "twistlock": True,
                    "type": [
                        "container",
                        "image",
                        "host_config",
                        "daemon_config",
                        "daemon_config_files",
                        "security_operations",
                        "k8s_master",
                        "k8s_worker",
                        "k8s_federation",
                        "linux",
                        "windows",
                        "istio",
                        "serverless",
                        "custom",
                        "docker_stig",
                        "openshift_master",
                        "openshift_worker",
                        "application_control_linux",
                        "gke_worker",
                        "image_malware",
                        "host_malware",
                        "aks_worker",
                        "eks_worker",
                        "image_secret",
                        "host_secret"
                    ],
                    "vecStr": "string",
                    "vulnTagInfos": [
                        {
                            "color": "string",
                            "comment": "string",
                            "name": "string"
                        }
                    ],
                    "wildfireMalware": {
                        "md5": "string",
                        "path": "string",
                        "verdict": "string"
                    }
                }
            ]
        }
    ],
    "hostDevices": [
        {
            "ip": "string",
            "name": "string"
        }
    ],
    "hostRuntimeEnabled": True,
    "hostname": "string",
    "hosts": {},
    "id": "string",
    "image": {
        "created": "2024-07-29T15:51:28.071Z",
        "entrypoint": [
          "string"
        ],
        "env": [
            "string"
        ],
        "healthcheck": True,
        "history": [
            {
                "baseLayer": True,
                "created": 0,
                "emptyLayer": True,
                "id": "string",
                "instruction": "string",
                "sizeBytes": 0,
                "tags": [
                    "string"
                ],
                "vulnerabilities": [
                    {
                        "applicableRules": [
                            "string"
                        ],
                        "binaryPkgs": [
                            "string"
                        ],
                        "block": True,
                        "cause": "string",
                        "cri": True,
                        "custom": True,
                        "cve": "string",
                        "cvss": 0,
                        "description": "string",
                        "discovered": "2024-07-29T15:51:28.071Z",
                        "exploit": [
                            "",
                            "exploit-db",
                            "exploit-windows",
                            "cisa-kev"
                        ],
                        "exploits": [
                            {
                                "kind": [
                                    "poc",
                                    "in-the-wild"
                                ],
                                "link": "string",
                                "source": [
                                    "",
                                    "exploit-db",
                                    "exploit-windows",
                                    "cisa-kev"
                                ]
                            }
                        ],
                        "fixDate": 0,
                        "fixLink": "string",
                        "functionLayer": "string",
                        "gracePeriodDays": 0,
                        "id": 0,
                        "layerTime": 0,
                        "link": "string",
                        "packageName": "string",
                        "packageType": [
                            "nodejs",
                            "gem",
                            "python",
                            "jar",
                            "package",
                            "windows",
                            "binary",
                            "nuget",
                            "go",
                            "app",
                            "unknown"
                        ],
                        "packageVersion": "string",
                        "published": 0,
                        "riskFactors": {},
                        "secret": {
                            "group": "string",
                            "locationInFile": "string",
                            "metadataModifiedTime": 0,
                            "modifiedTime": 0,
                            "originalFileLocation": "string",
                            "path": "string",
                            "permissions": "string",
                            "secretID": "string",
                            "size": 0,
                            "snippet": "string",
                            "type": [
                                "AWS Access Key ID",
                                "AWS Secret Key",
                                "AWS MWS Auth Token",
                                "Azure Storage Account Access Key",
                                "Azure Service Principal",
                                "GCP Service Account Auth Key",
                                "Private Encryption Key",
                                "Public Encryption Key",
                                "PEM X509 Certificate Header",
                                "SSH Authorized Keys",
                                "Artifactory API Token",
                                "Artifactory Password",
                                "Basic Auth Credentials",
                                "Mailchimp Access Key",
                                "NPM Token",
                                "Slack Token",
                                "Slack Webhook",
                                "Square OAuth Secret",
                                "Notion Integration Token",
                                "Airtable API Key",
                                "Atlassian Oauth2 Keys",
                                "CircleCI Personal Token",
                                "Databricks Authentication Token",
                                "GitHub Token",
                                "GitLab Token",
                                "Google API key",
                                "Grafana Token",
                                "Python Package Index Key (PYPI)",
                                "Typeform API Token",
                                "Scalr Token",
                                "Braintree Access Token",
                                "Braintree Payments Key",
                                "Paypal Token Key",
                                "Braintree Payments ID",
                                "Datadog Client Token",
                                "ClickUp Personal API Token",
                                "OpenAI API Key",
                                "Java DB Connectivity (JDBC)",
                                "MongoDB",
                                ".Net SQL Server"
                            ],
                            "user": "string"
                        },
                        "severity": "string",
                        "status": "string",
                        "templates": [
                            [
                                "PCI",
                                "HIPAA",
                                "NIST SP 800-190",
                                "GDPR",
                                "DISA STIG"
                            ]
                        ],
                        "text": "string",
                        "title": "string",
                        "twistlock": True,
                        "type": [
                            "container",
                            "image",
                            "host_config",
                            "daemon_config",
                            "daemon_config_files",
                            "security_operations",
                            "k8s_master",
                            "k8s_worker",
                            "k8s_federation",
                            "linux",
                            "windows",
                            "istio",
                            "serverless",
                            "custom",
                            "docker_stig",
                            "openshift_master",
                            "openshift_worker",
                            "application_control_linux",
                            "gke_worker",
                            "image_malware",
                            "host_malware",
                            "aks_worker",
                            "eks_worker",
                            "image_secret",
                            "host_secret"
                        ],
                        "vecStr": "string",
                        "vulnTagInfos": [
                            {
                                "color": "string",
                                "comment": "string",
                                "name": "string"
                            }
                        ],
                        "wildfireMalware": {
                            "md5": "string",
                            "path": "string",
                            "verdict": "string"
                        }
                    }
                ]
            }
        ],
        "id": "string",
        "labels": {},
        "layers": [
            "string"
        ],
        "os": "string",
        "repoDigest": [
            "string"
        ],
        "repoTags": [
            "string"
        ],
        "user": "string",
        "workingDir": "string"
    },
    "installedProducts": {
        "agentless": True,
        "apache": "string",
        "awsCloud": True,
        "clusterType": [
            "AKS",
            "ECS",
            "EKS",
            "GKE",
            "Kubernetes"
        ],
        "crio": True,
        "docker": "string",
        "dockerEnterprise": True,
        "hasPackageManager": True,
        "k8sApiServer": True,
        "k8sControllerManager": True,
        "k8sEtcd": True,
        "k8sFederationApiServer": True,
        "k8sFederationControllerManager": True,
        "k8sKubelet": True,
        "k8sProxy": True,
        "k8sScheduler": True,
        "kubernetes": "string",
        "managedClusterVersion": "string",
        "openshift": True,
        "openshiftVersion": "string",
        "osDistro": "string",
        "serverless": True,
        "swarmManager": True,
        "swarmNode": True
    },
    "instances": [
        {
            "host": "string",
            "image": "string",
            "modified": "2024-07-29T15:51:28.071Z",
            "registry": "string",
            "repo": "string",
            "tag": "string"
        }
    ],
    "isARM64": True,
    "k8sClusterAddr": "string",
    "labels": [
        "string"
    ],
    "layers": [
        "string"
    ],
    "malwareAnalyzedTime": "2024-07-29T15:51:28.071Z",
    "missingDistroVulnCoverage": True,
    "namespaces": [
        "string"
    ],
    "osDistro": "string",
    "osDistroRelease": "string",
    "osDistroVersion": "string",
    "packageManager": True,
    "packages": [
        {
            "pkgs": [
                {
                    "author": "string",
                    "binaryIdx": [
                        0
                    ],
                    "binaryPkgs": [
                        "string"
                    ],
                    "cveCount": 0,
                    "defaultGem": True,
                    "files": [
                        {
                            "md5": "string",
                            "original_file_location": "string",
                            "path": "string",
                            "sha1": "string",
                            "sha256": "string"
                        }
                    ],
                    "functionLayer": "string",
                    "goPkg": True,
                    "jarIdentifier": "string",
                    "layerTime": 0,
                    "license": "string",
                    "name": "string",
                    "originPackageName": "string",
                    "osPackage": True,
                    "path": "string",
                    "purl": "string",
                    "securityRepoPkg": True,
                    "symbols": [
                        "string"
                    ],
                    "version": "string"
                }
            ],
            "pkgsType": [
                "nodejs",
                "gem",
                "python",
                "jar",
                "package",
                "windows",
                "binary",
                "nuget",
                "go",
                "app",
                "unknown"
            ]
        }
    ],
    "pullDuration": 0,
    "pushTime": "2024-07-29T15:51:28.071Z",
    "redHatNonRPMImage": True,
    "registryNamespace": "string",
    "registryTags": [
        "string"
    ],
    "registryType": "string",
    "repoDigests": [
        "string"
    ],
    "repoTag": {
        "digest": "string",
        "id": "string",
        "registry": "string",
        "repo": "string",
        "tag": "string"
    },
    "rhelRepos": [
        "string"
    ],
    "riskFactors": {},
    "scanBuildDate": "string",
    "scanDuration": 0,
    "scanID": 0,
    "scanTime": "2024-07-29T15:51:28.071Z",
    "scanVersion": "string",
    "secretScanMetrics": {
        "failedScans": 0,
        "foundSecrets": 0,
        "scanTime": 0,
        "scanTimeouts": 0,
        "scannedFileSize": 0,
        "scannedFiles": 0,
        "totalBytes": 0,
        "totalFiles": 0,
        "totalTime": 0,
        "typesCount": {}
    },
    "startupBinaries": [
        {
            "altered": True,
            "cveCount": 0,
            "deps": [
                "string"
            ],
            "fileMode": 0,
            "functionLayer": "string",
            "md5": "string",
            "missingPkg": True,
            "name": "string",
            "path": "string",
            "pkgRootDir": "string",
            "services": [
                "string"
            ],
            "version": "string"
        }
    ],
    "stopped": True,
    "tags": [
        {
            "digest": "string",
            "id": "string",
            "registry": "string",
            "repo": "string",
            "tag": "string"
        }
    ],
    "topLayer": "string",
    "trustResult": {
        "groups": [
            {
                "_id": "string",
                "disabled": True,
                "images": [
                    "string"
                ],
                "layers": [
                    "string"
                ],
                "modified": "2024-07-29T15:51:28.071Z",
                "name": "string",
                "notes": "string",
                "owner": "string",
                "previousName": "string"
            }
        ],
        "hostsStatuses": [
            {
                "host": "string",
                "status": [
                    "trusted",
                    "untrusted"
                ]
            }
        ]
    },
    "trustStatus": [
        "trusted",
        "untrusted"
    ],
    "twistlockImage": True,
    "type": [
        "image",
        "ciImage",
        "container",
        "host",
        "agentlessHost",
        "registry",
        "serverlessScan",
        "ciServerless",
        "vm",
        "tas",
        "ciTas",
        "cloudDiscovery",
        "serverlessRadar",
        "serverlessAutoDeploy",
        "hostAutoDeploy",
        "codeRepo",
        "ciCodeRepo"
    ],
    "underlyingDistro": "string",
    "underlyingDistroRelease": "string",
    "vulnerabilities": [
        {
            "applicableRules": [
                "string"
            ],
            "binaryPkgs": [
                "string"
            ],
            "block": True,
            "cause": "string",
            "cri": True,
            "custom": True,
            "cve": "string",
            "cvss": 0,
            "description": "string",
            "discovered": "2024-07-29T15:51:28.071Z",
            "exploit": [
                "",
                "exploit-db",
                "exploit-windows",
                "cisa-kev"
            ],
            "exploits": [
                {
                    "kind": [
                        "poc",
                        "in-the-wild"
                    ],
                    "link": "string",
                    "source": [
                        "",
                        "exploit-db",
                        "exploit-windows",
                        "cisa-kev"
                    ]
                }
            ],
            "fixDate": 0,
            "fixLink": "string",
            "functionLayer": "string",
            "gracePeriodDays": 0,
            "id": 0,
            "layerTime": 0,
            "link": "string",
            "packageName": "string",
            "packageType": [
                "nodejs",
                "gem",
                "python",
                "jar",
                "package",
                "windows",
                "binary",
                "nuget",
                "go",
                "app",
                "unknown"
            ],
            "packageVersion": "string",
            "published": 0,
            "riskFactors": {},
            "secret": {
                "group": "string",
                "locationInFile": "string",
                "metadataModifiedTime": 0,
                "modifiedTime": 0,
                "originalFileLocation": "string",
                "path": "string",
                "permissions": "string",
                "secretID": "string",
                "size": 0,
                "snippet": "string",
                "type": [
                    "AWS Access Key ID",
                    "AWS Secret Key",
                    "AWS MWS Auth Token",
                    "Azure Storage Account Access Key",
                    "Azure Service Principal",
                    "GCP Service Account Auth Key",
                    "Private Encryption Key",
                    "Public Encryption Key",
                    "PEM X509 Certificate Header",
                    "SSH Authorized Keys",
                    "Artifactory API Token",
                    "Artifactory Password",
                    "Basic Auth Credentials",
                    "Mailchimp Access Key",
                    "NPM Token",
                    "Slack Token",
                    "Slack Webhook",
                    "Square OAuth Secret",
                    "Notion Integration Token",
                    "Airtable API Key",
                    "Atlassian Oauth2 Keys",
                    "CircleCI Personal Token",
                    "Databricks Authentication Token",
                    "GitHub Token",
                    "GitLab Token",
                    "Google API key",
                    "Grafana Token",
                    "Python Package Index Key (PYPI)",
                    "Typeform API Token",
                    "Scalr Token",
                    "Braintree Access Token",
                    "Braintree Payments Key",
                    "Paypal Token Key",
                    "Braintree Payments ID",
                    "Datadog Client Token",
                    "ClickUp Personal API Token",
                    "OpenAI API Key",
                    "Java DB Connectivity (JDBC)",
                    "MongoDB",
                    ".Net SQL Server"
                ],
                "user": "string"
            },
            "severity": "string",
            "status": "string",
            "templates": [
                [
                    "PCI",
                    "HIPAA",
                    "NIST SP 800-190",
                    "GDPR",
                    "DISA STIG"
                ]
            ],
            "text": "string",
            "title": "string",
            "twistlock": True,
            "type": [
                "container",
                "image",
                "host_config",
                "daemon_config",
                "daemon_config_files",
                "security_operations",
                "k8s_master",
                "k8s_worker",
                "k8s_federation",
                "linux",
                "windows",
                "istio",
                "serverless",
                "custom",
                "docker_stig",
                "openshift_master",
                "openshift_worker",
                "application_control_linux",
                "gke_worker",
                "image_malware",
                "host_malware",
                "aks_worker",
                "eks_worker",
                "image_secret",
                "host_secret"
            ],
            "vecStr": "string",
            "vulnTagInfos": [
                {
                    "color": "string",
                    "comment": "string",
                    "name": "string"
                }
            ],
            "wildfireMalware": {
                "md5": "string",
                "path": "string",
                "verdict": "string"
            }
        }
    ],
    "vulnerabilitiesCount": 0,
    "vulnerabilityDistribution": {
        "critical": 0,
        "high": 0,
        "low": 0,
        "medium": 0,
        "total": 0
    },
    "vulnerabilityRiskScore": 0,
    "wildFireUsage": {
        "bytes": 0,
        "queries": 0,
        "uploads": 0
    }
}
