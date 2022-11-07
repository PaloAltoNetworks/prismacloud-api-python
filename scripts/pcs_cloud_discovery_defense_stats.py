""" Get statistics from cloud discovery """

# pylint: disable=import-error
import pprint

from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
parser.add_argument(
    '--fargate',
    action="store_true",
    help="(Optional) - Only Fargate stats"
)
parser.add_argument(
    '--eks',
    action="store_true",
    help="(Optional) - Only EKS stats"
)
parser.add_argument(
    '--detailed',
    action="store_true",
    help="(Optional) - Detailed results"
)
args = parser.parse_args()

# --Helpers-- #


# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Note: default provider is aws
# To-do: support other cloud providers

discovery = pc_api.cloud_discovery_read()

aws_ec2 = 0
aws_ec2_defended = 0
aws_lambda = 0
aws_lambda_defended = 0
aws_ecs = 0
aws_ecs_defended = 0
aws_eks = 0
aws_eks_defended = 0
aws_eks_clusters = []
aws_ecr = 0
aws_ecr_defended = 0

print('Account, Region, Service, Defended Count, Total Count')
services = {'aws-ec2', 'aws-lambda','aws-ecs','aws-eks','aws-ecr'}
if args.fargate:
    services = {'aws-fargate'}
elif args.eks:
    services = {'aws-eks'}
for item in discovery:
    if 'err' in item:
        continue
    if item['provider'] == 'aws':
        service = item['serviceType']
        if service not in services:
            continue
        if service == 'aws-ec2':
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_ec2 += item['total']
            aws_ec2_defended += item['defended']
        elif service == 'aws-lambda':
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_lambda += item['total']
            aws_lambda_defended += item['defended']
        elif service == 'aws-ecs':
#            pprint.pprint(item)
            for entity in item['entities']:
                print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], entity['runningTasksCount']))
                aws_ecs += entity['runningTasksCount']
                aws_ecs_defended += item['defended']
        elif service == 'aws-eks':
#            pprint.pprint(item)
            if args.detailed:
                item.pop('collections')
            if args.detailed:
                aws_eks_clusters.append(item)
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_eks += item['total']
            aws_eks_defended += item['defended']
        elif service == 'aws-ecr':
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_ecr += item['total']
            aws_ecr_defended += item['defended']
        else:
            print('Unknown AWS service: %s' % service)

if not args.detailed:
    print('Totals')
    print('EC2: %d/%d' % (aws_ec2_defended, aws_ec2))
    print('EKS: %d/%d' % (aws_eks_defended, aws_eks))
    print('Lambda: %d/%d' % (aws_lambda_defended, aws_lambda))
    print('ECS tasks: %d/%d' % (aws_ecs_defended, aws_ecs))
    print('ECR: %d/%d' % (aws_ecr_defended, aws_ecr))

if args.eks and args.detailed:
    print('EKS: %d/%d' % (aws_eks_defended, aws_eks))
    print('Account, Region, Cluster, Defended, ARN')
    for item in aws_eks_clusters:
        for entity in item['entities']:
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], entity['name'], item['defended'], entity['arn']))
            
