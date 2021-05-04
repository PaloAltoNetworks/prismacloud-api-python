import os
import yaml

class ConfigHelper(object):
    def __init__(self):
        config = self.read_yml('configs')
        self.rl_user = config["prisma_cloud"]["username"]
        self.rl_pass = config["prisma_cloud"]["password"]
        self.rl_cust = config["prisma_cloud"]["customer_name"]
        self.rl_api_base = config["prisma_cloud"]["api_base"]
        self.rl_ca_bundle = config["prisma_cloud"]["ca_bundle"]
        self.rl_file_name = config["prisma_cloud"]["filename"]

    @classmethod
    def read_yml(self, f):
        yml_path = os.path.join(os.path.dirname(__file__), "../config/%s.yml" % f)
        with open(yml_path,'r') as stream:
            return yaml.safe_load(stream)
