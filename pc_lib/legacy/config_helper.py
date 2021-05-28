""" Legacy SDK Version 1.0: Configuration """

import os
import yaml

class ConfigHelper():
    """ Legacy SDK Version 1.0: Configuration """

    # pylint: disable=useless-return
    def __init__(self):
        config = self.read_yml()
        self.rl_user      = config['prisma_cloud']['username']
        self.rl_pass      = config['prisma_cloud']['password']
        self.rl_cust      = config['prisma_cloud']['customer_name']
        self.rl_api_base  = config['prisma_cloud']['api_base']
        self.rl_ca_bundle = config['prisma_cloud']['ca_bundle']
        self.rl_file_name = config['prisma_cloud']['filename']
        return None

    @classmethod
    # pylint: disable=invalid-name
    def read_yml(cls, f='configs.yml', d=None):
        if not d:
            d = os.path.join(os.getcwd(), 'config')
        yaml_file = '%s/%s' % (d, f)
        with open(yaml_file, 'r') as stream:
            return yaml.safe_load(stream)

    @classmethod
    # pylint: disable=invalid-name,useless-return
    def write_yml(cls, config=None, f='configs.yml', d=None):
        if not config:
            config = {'prisma_cloud': {}}
            config['prisma_cloud']['username']      = ''
            config['prisma_cloud']['password']      = ''
            config['prisma_cloud']['customer_name'] = ''
            config['prisma_cloud']['api_base']      = ''
            config['prisma_cloud']['ca_bundle']     = ''
            config['prisma_cloud']['filename']      = ''
        if not d:
            d = os.path.join(os.getcwd(), 'config')
        yaml_file = '%s/%s' % (d, f)
        with open(yaml_file, 'w') as stream:
            yaml.dump(config, stream)
        return None
