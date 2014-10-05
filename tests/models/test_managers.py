from ..base import BaseTestCase

from ec2.models.managers import (
    InstanceManager,
    SecurityGroupManager,
    VPCManager)


class InstancesTestCase(BaseTestCase):
    def test_all(self):
        "instances.all() should iterate over all reservations and collect all instances, then cache the results"
        with self._patch_connection() as mock:
            instances = InstanceManager.all()
            self.assertEquals(4, len(instances))
            # all() should cache the connection and list of instances
            # so when calling a second time, _connect() shouldn't
            # be called
            InstanceManager.all()
            mock.assert_called_once()  # Should only be called once from the initial _connect

    def test_filters_integration(self):
        with self._patch_connection():
            instances = InstanceManager.filter(state='crap')
            self.assertEquals(0, len(instances))

            instances = InstanceManager.filter(state='running')
            self.assertEquals(2, len(instances))
            self.assertEquals('running', instances[0].state)
            self.assertEquals('running', instances[1].state)

            instances = InstanceManager.filter(state='stopped')
            self.assertEquals(2, len(instances))
            self.assertEquals('stopped', instances[0].state)
            self.assertEquals('stopped', instances[1].state)

            instances = InstanceManager.filter(id__exact='i-abc0')
            self.assertEquals(1, len(instances))

            instances = InstanceManager.filter(id__iexact='I-ABC0')
            self.assertEquals(1, len(instances))

            instances = InstanceManager.filter(id__like=r'^i\-abc\d$')
            self.assertEquals(4, len(instances))

            instances = InstanceManager.filter(id__ilike=r'^I\-ABC\d$')
            self.assertEquals(4, len(instances))

            instances = InstanceManager.filter(id__contains='1')
            self.assertEquals(1, len(instances))

            instances = InstanceManager.filter(id__icontains='ABC')
            self.assertEquals(4, len(instances))

            instances = InstanceManager.filter(id__startswith='i-')
            self.assertEquals(4, len(instances))

            instances = InstanceManager.filter(id__istartswith='I-')
            self.assertEquals(4, len(instances))

            instances = InstanceManager.filter(id__endswith='c0')
            self.assertEquals(1, len(instances))

            instances = InstanceManager.filter(id__iendswith='C0')
            self.assertEquals(1, len(instances))

            instances = InstanceManager.filter(id__startswith='i-', name__endswith='-0')
            self.assertEquals(1, len(instances))

            instances = InstanceManager.filter(id__isnull=False)
            self.assertEquals(4, len(instances))

            instances = InstanceManager.filter(id__isnull=True)
            self.assertEquals(0, len(instances))

    def test_get_raises(self):
        with self._patch_connection():
            self.assertRaises(
                InstanceManager.MultipleObjectsReturned,
                InstanceManager.get,
                id__startswith='i'
            )

            self.assertRaises(
                InstanceManager.DoesNotExist,
                InstanceManager.get,
                name='crap'
            )

    def test_get(self):
        with self._patch_connection():
            self.assertEquals(InstanceManager.get(id='i-abc0').id, 'i-abc0')

    def test_create(self):
        instance = InstanceManager.create('')
        self.assertEquals('i-abc1', instance.id)

    def test_delete(self):
        result = InstanceManager.delete('')
        print result


class SecurityGroupManagerTestCase(BaseTestCase):
    def test_all(self):
        with self._patch_connection() as mock:
            groups = SecurityGroupManager.all()
            print groups
            self.assertEquals(2, len(groups))
            # all() should cache the connection and list of instances
            # so when calling a second time, _connect() shouldn't
            # be called
            SecurityGroupManager.all()
            mock.assert_called_once()

    def test_filters_integration(self):
        with self._patch_connection():
            groups = SecurityGroupManager.filter(name='crap')
            self.assertEquals(0, len(groups))

            groups = SecurityGroupManager.filter(id__exact='sg-abc0')
            self.assertEquals(1, len(groups))

            groups = SecurityGroupManager.filter(id__iexact='SG-ABC0')
            self.assertEquals(1, len(groups))

            groups = SecurityGroupManager.filter(id__like=r'^sg\-abc\d$')
            self.assertEquals(2, len(groups))

            groups = SecurityGroupManager.filter(id__ilike=r'^SG\-ABC\d$')
            self.assertEquals(2, len(groups))

            groups = SecurityGroupManager.filter(id__contains='1')
            self.assertEquals(1, len(groups))

            groups = SecurityGroupManager.filter(id__icontains='ABC')
            self.assertEquals(2, len(groups))

            groups = SecurityGroupManager.filter(id__startswith='sg-')
            self.assertEquals(2, len(groups))

            groups = SecurityGroupManager.filter(id__istartswith='SG-')
            self.assertEquals(2, len(groups))

            groups = SecurityGroupManager.filter(id__endswith='c0')
            self.assertEquals(1, len(groups))

            groups = SecurityGroupManager.filter(id__iendswith='C0')
            self.assertEquals(1, len(groups))

            groups = SecurityGroupManager.filter(id__startswith='sg-', name__endswith='-0')
            self.assertEquals(1, len(groups))

            groups = SecurityGroupManager.filter(id__isnull=False)
            self.assertEquals(2, len(groups))

            groups = SecurityGroupManager.filter(id__isnull=True)
            self.assertEquals(0, len(groups))

    def test_get_raises(self):
        with self._patch_connection():
            self.assertRaises(
                SecurityGroupManager.MultipleObjectsReturned,
                SecurityGroupManager.get,
                id__startswith='sg'
            )

            self.assertRaises(
                SecurityGroupManager.DoesNotExist,
                SecurityGroupManager.get,
                name='crap'
            )

    def test_get(self):
        with self._patch_connection():
            self.assertEquals(SecurityGroupManager.get(id='sg-abc0').id, 'sg-abc0')

    def test_create(self):
        with self._patch_connection():
            sg = SecurityGroupManager.create('sg-99', 'Group 99')
            self.assertEquals(sg.id, 'sg-xyz0')

    def test_delete(self):
        with self._patch_connection():
            sg = SecurityGroupManager.create('sg-99', 'Group 99')
            self.assertTrue(SecurityGroupManager.delete(sg.id))


class VPCTestCase(BaseTestCase):
    def test_all(self):
        with self._patch_vpc_connection() as mock:
            vpcs = VPCManager.all()
            self.assertEquals(2, len(vpcs))
            VPCManager.all()
            mock.assert_called_once()

    def test_filters_integration(self):
        with self._patch_vpc_connection():
            groups = VPCManager.filter(id__exact='vpc-abc0')
            self.assertEquals(1, len(groups))

            groups = VPCManager.filter(id__iexact='VPC-ABC0')
            self.assertEquals(1, len(groups))

            groups = VPCManager.filter(id__like=r'^vpc\-abc\d$')
            self.assertEquals(2, len(groups))

            groups = VPCManager.filter(id__ilike=r'^VPC\-ABC\d$')
            self.assertEquals(2, len(groups))

            groups = VPCManager.filter(id__contains='1')
            self.assertEquals(1, len(groups))

            groups = VPCManager.filter(id__icontains='ABC')
            self.assertEquals(2, len(groups))

            groups = VPCManager.filter(id__startswith='vpc-')
            self.assertEquals(2, len(groups))

            groups = VPCManager.filter(id__istartswith='vpc-')
            self.assertEquals(2, len(groups))

            groups = VPCManager.filter(id__endswith='c0')
            self.assertEquals(1, len(groups))

            groups = VPCManager.filter(id__iendswith='C0')
            self.assertEquals(1, len(groups))

            groups = VPCManager.filter(id__startswith='vpc-', dhcp_options_id__endswith='abc0')
            self.assertEquals(1, len(groups))

            groups = VPCManager.filter(id__isnull=False)
            self.assertEquals(2, len(groups))

            groups = VPCManager.filter(id__isnull=True)
            self.assertEquals(0, len(groups))

    def test_get_raises(self):
        with self._patch_vpc_connection():
            self.assertRaises(
                VPCManager.MultipleObjectsReturned,
                VPCManager.get,
                id__startswith='vpc'
            )

            self.assertRaises(
                VPCManager.DoesNotExist,
                VPCManager.get,
                name='crap'
            )

    def test_get(self):
        with self._patch_vpc_connection():
            self.assertEquals(VPCManager.get(id='vpc-abc0').id, 'vpc-abc0')

    def test_create(self):
        with self._patch_vpc_connection():
            vpc = VPCManager.create('10.10.10.0/16')
            self.assertEquals(vpc.id, 'vpc-xyz0')

    def test_delete(self):
        with self._patch_vpc_connection():
            vpc = VPCManager.create('10.10.10.0/16')
            self.assertTrue(VPCManager.delete(vpc.id))
