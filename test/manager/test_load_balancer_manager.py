import unittest
import time
import os
from datetime import datetime, timedelta
from unittest.mock import patch
from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core import utils
from spaceone.inventory.error import *
from spaceone.inventory.connector.loadbalncer import LoadBalancerConnector
from spaceone.inventory.manager.loadbalancer_manager import LoadBalancerManager


class TestLoadBalancerManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.monitoring')

        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})

        cls.load_balancer_connector = LoadBalancerConnector(transaction=Transaction(), config={}, secret_data=cls.azure_credentials)

        cls.load_balancer_manager = LoadBalancerManager(Transaction())

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_collect_cloud_service(self, *args):
        secret_data = self.azure_credentials

        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        load_balancers = self.load_balancer_manager.collect_cloud_service(params)

        for load_balancer in load_balancers:
            print(load_balancer.to_primitive())


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)