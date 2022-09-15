""" Get statistics from cloud discovery """

# pylint: disable=import-error
from prismacloud.api import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()
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
aws_ecr = 0
aws_ecr_defended = 0

print('Account, Region, Service, Defended Count, Total Count')
for item in discovery:
    if 'err' in item:
        continue
    if item['provider'] == 'aws':
        service = item['serviceType']
        if service == 'aws-ec2':
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_ec2 += item['total']
            aws_ec2_defended += item['defended']
        elif service == 'aws-lambda':
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_lambda += item['total']
            aws_lambda_defended += item['defended']
        elif service == 'aws-ecs':
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_ecs += item['total']
            aws_ecs_defended += item['defended']
        elif service == 'aws-eks':
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_eks += item['total']
            aws_eks_defended += item['defended']
        elif service == 'aws-ecr':
            print('%s, %s, %s, %s, %s' % (item['accountID'], item['region'], service, item['defended'], item['total']))
            aws_ecr += item['total']
            aws_ecr_defended += item['defended']
        else:
            print('unknown service: %s' % service)

print('Totals')
print('EC2: %d/%d' % (aws_ec2_defended, aws_ec2))
print('EKS: %d/%d' % (aws_eks_defended, aws_eks))
print('Lambda: %d/%d' % (aws_lambda_defended, aws_lambda))
print('ECS: %d/%d' % (aws_ecs_defended, aws_ecs))
print('ECR: %d/%d' % (aws_ecr_defended, aws_ecr))
