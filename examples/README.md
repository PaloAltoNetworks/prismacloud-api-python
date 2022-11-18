## Support

This project has been developed by Prisma Cloud SEs, it is not Supported by Palo Alto Networks.
Nevertheless, the maintainers will make a best-effort to address issues, and (of course) contributors are encouraged to submit issues and pull requests.

## Example Script

Prior to running the script ensure that the prismacloud-api is configured to run as described in [README.md](#scripts/README.md)

### pcs_vuln_container_with_cve_2022_22965.py

List packages that contain CVE-2022-22965 and JDK **other than** 1.8.
The results are stored to a *CVE-2022-22965-WITHOUT-JAVA8.csv* in the same directory.

```
python3 pcs_vuln_container_with_cve_2022_22965.py
```
