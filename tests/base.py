from boto.ec2.instance import Instance, InstanceState

from boto.ec2.securitygroup import SecurityGroup
from boto.vpc.vpc import VPC
from mock import MagicMock, patch
import unittest

import ec2

RUNNING_STATE = InstanceState(16, 'running')
STOPPED_STATE = InstanceState(64, 'stopped')


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        ec2.credentials.ACCESS_KEY_ID = 'abc'
        ec2.credentials.SECRET_ACCESS_KEY = 'xyz'

        # Build up two reservations, with two instances each, totalling 4 instances
        # Two running, two stopped
        reservations = []
        instance_count = 0
        for i in xrange(2):
            i1 = Instance()
            i1.id = 'i-abc%d' % instance_count
            i1._state = RUNNING_STATE
            i1.tags = {'Name': 'instance-%d' % instance_count}
            instance_count += 1
            i2 = Instance()
            i2.id = 'i-abc%d' % instance_count
            i2._state = STOPPED_STATE
            i2.tags = {'Name': 'instance-%d' % instance_count}
            instance_count += 1
            reservation = MagicMock()
            reservation.instances.__iter__ = MagicMock(return_value=iter([i1, i2]))
            reservations.append(reservation)

        security_groups = []
        for i in xrange(2):
            sg = SecurityGroup()
            sg.id = 'sg-abc%d' % i
            sg.name = 'group-%d' % i
            sg.description = 'Group %d' % i
            security_groups.append(sg)

        created_sg = SecurityGroup()
        created_sg.id = 'sg-xyz0'
        created_sg.name = 'group-99'
        created_sg.description = 'Group 99'

        for sg in security_groups:
            sg.delete = MagicMock(return_value=True)

        vpcs = []
        for i in xrange(2):
            vpc = VPC()
            vpc.id = 'vpc-abc%d' % i
            if i % 2:
                vpc.state = 'pending'
                vpc.is_default = False
                vpc.instance_tenancy = 'default'
            else:
                vpc.state = 'available'
                vpc.is_default = True
                vpc.instance_tenancy = 'dedicated'
            vpc.cidr_block = '10.%d.0.0/16' % i
            vpc.dhcp_options_id = 'dopt-abc%d' % i
            vpcs.append(vpc)

        created_vpc = VPC()
        created_vpc.id = 'vpc-xyz0'
        created_vpc.state = 'pending'
        created_vpc.is_default = False
        created_vpc.instance_tenancy = 'default'
        created_vpc.cidr_block = '10.10.10.0/16'
        created_vpc.dhcp_options_id = 'dopt-xyz0'

        self.connection = MagicMock()
        self.connection.get_all_instances = MagicMock(return_value=reservations)
        self.connection.get_all_security_groups = MagicMock(return_value=security_groups)
        self.connection.create_security_group = MagicMock(return_value=created_sg)
        self.connection.run_instances = MagicMock(return_value=i1)

        self.vpc_connection = MagicMock()
        self.vpc_connection.get_all_vpcs = MagicMock(return_value=vpcs)
        self.vpc_connection.create_vpc = MagicMock(return_value=created_vpc)

        for v in vpcs:
            v.delete = MagicMock(return_value=True)

    def tearDown(self):
        ec2.credentials.ACCESS_KEY_ID = None
        ec2.credentials.SECRET_ACCESS_KEY = None
        ec2.credentials.REGION_NAME = 'us-east-1'
        # ec2.instances.clear()
        # ec2.security_groups.clear()
        # ec2.vpcs.clear()

    def _patch_connection(self):
        return patch('ec2.models.managers.get_connection', return_value=self.connection)

    def _patch_vpc_connection(self):
        return patch('ec2.models.managers.get_vpc_connection', return_value=self.vpc_connection)
