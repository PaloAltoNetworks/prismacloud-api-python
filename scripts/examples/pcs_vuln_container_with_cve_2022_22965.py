""" Get a list of vulnerable containers and their clusters """
import os
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--cve',
    type=str,
    required=False,
    default='CVE-2022-22965',
    help='(Required) - ID of the CVE.')
parser.add_argument(
    '--image_id',
    type=str,
    help='(Optional) - ID of the Image (sha256:...).')
parser.add_argument(
    '--mode',
    type=str,
    choices=['registry', 'deployed', 'all'],
    default='all',
    help='(Optional) - Report on Registry, Deployed, or all Images.')
args = parser.parse_args()

# --Helpers-- #

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)
pc_api.validate_api_compute()

# --Main-- #

print('Testing Compute API Access ...', end='')
intelligence = pc_api.statuses_intelligence()
print(' done.')
print()

print('Searching for CVE: (%s) Limiting Search to Image ID: (%s)' % (args.cve, args.image_id))
print()

#Image_ID, Registry, Repo, Tag, CVE_ID, Application, Version, path 
vulnerableImageDetails = []
vulnerableImageDetails.append("Image_ID,Registry,Repo,Tag,CVE_ID,Application,Version,Path\n")

# Monitor > Vulnerabilities/Compliance > Images > Registries
if args.mode in ['registry', 'all']:
    registry_images = pc_api.registry_list_read(args.image_id)
    print('Getting Registry Images ...', end='')
    print(' done.')
    print('Found %s Registry Images' % len(registry_images))
    print()
    for image in registry_images:
        image_id = image['_id']
        vulnerabilities = image['vulnerabilities']
        if not vulnerabilities:
            # print('No vulnerabilities for Image ID: %s' % image_id)
            continue
        vulnerable = False
        for vulnerability in vulnerabilities:
            if args.cve and vulnerability['cve'] == args.cve:
                vulnerable = True
                # print('Image ID: %s is vulnerable to CVE: %s' % (image_id, args.cve))
                #check if it contains the java application
                if 'applications' in image:
                    for app in image['applications']:
                        if ((app['name'] == 'java') and ('1.8' not in app['version'])):
                            _registry = image['tags'][0]['registry']
                            _repo = image['tags'][0]['repo']
                            _tag = image['tags'][0]['tag']
                            _vulnerabilityDetails = image['_id'] + ',' + _registry + ',' + _repo + ',' + _tag + ',' + vulnerability['cve'] + ',' + app['name'] + ',' + app['version'] + ',' + app['path'] + '\n'
                            vulnerableImageDetails.append(_vulnerabilityDetails)
                            #print('Applicaiton Name: %s' % app)
                            #print('Image ID: %s is vulnerable to CVE: %s' % (image_id, args.cve))
                            #print('Registry: %s' % image['tags'])
                            break
                break
    print()

# Monitor > Vulnerabilities/Compliance > Images > Deployed
if args.mode in ['deployed', 'all']:
    print('Getting Deployed Images ...', end='')
    deployed_images = pc_api.images_list_read(image_id=args.image_id, query_params={'filterBaseImage': 'true'})
    print(' done.')
    print('Found %s Deployed Images' % len(deployed_images))
    print()
    #Image_ID, Registry, Repo, Tag, CVE_ID, Application, Version, path 
    #vulnerableImageDetails = []
    vulnerableImageDetails.append("Image_ID,Registry,Repo,Tag,CVE_ID,Application,Version,Path\n")
    for image in deployed_images:
        image_id = image['_id']
        vulnerabilities = image['vulnerabilities']

        if not vulnerabilities:
            # print('No vulnerabilities for Image ID: %s' % image_id)
            continue
        vulnerable = False
        for vulnerability in vulnerabilities:
            if args.cve and vulnerability['cve'] == args.cve:
                vulnerable = True
                #check if it contains the java application 
                if 'applications' in image:
                    for app in image['applications']:
                        if ((app['name'] == 'java') and ('1.8' not in app['version'])):
                            _registry = image['tags'][0]['registry']
                            _repo = image['tags'][0]['repo']
                            _tag = image['tags'][0]['tag']
                            _vulnerabilityDetails = image['_id'] + ',' + _registry + ',' + _repo + ',' + _tag + ',' + vulnerability['cve'] + ',' + app['name'] + ',' + app['version'] + ',' + app['path'] + '\n'
                            vulnerableImageDetails.append(_vulnerabilityDetails)
                            #print('Applicaiton Name: %s' % app)
                            #print('Image ID: %s is vulnerable to CVE: %s' % (image_id, args.cve))
                            #print('Registry: %s' % image['tags'])
                            break
                break
    print()
    #print(vulnerableImageDetails)

    file_name_and_path = os.path.join(os.getcwd(), 'CVE-2022-22965-WITHOUT-JAVA8.csv')
    try:
        with open(file_name_and_path, 'w') as file:
            for line in vulnerableImageDetails:
                file.write(line)
    except Exception as ex:
            print('Failed to write csv file. %s', ex)