import unittest

from moto import mock_ec2

from ec2.models import SecurityGroup


class SecurityGroupModelTestCase(unittest.TestCase):
    @mock_ec2
    def test_sg_create(self):
        name = 'test_create'
        description = 'test_create sg'
        sg_all = SecurityGroup.objects.all()
        sg_all2 = SecurityGroup.objects.all()
        self.assertEqual(sg_all, sg_all2)
        sg = SecurityGroup.objects.create(name=name, description=description)
        self.assertIn(sg, SecurityGroup.objects.all())
        self.assertEquals(sg.name, name)
        self.assertEquals(sg.description, description)

        # ensure original methods are in place
        self.assertTrue(hasattr(sg, 'authorize'))

        # ensure our added methods are in place
        self.assertTrue(hasattr(sg, 'delete'))

    @mock_ec2
    def test_sg_delete(self):
        pass

    @mock_ec2
    def test_sg_all(self):
        pass
