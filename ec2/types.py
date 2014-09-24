"""
ec2.types
~~~~~~~~~

:copyright: (c) 2014 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""

from ec2.connection import get_connection, get_vpc_connection
from ec2.base import objects_base


class instances(objects_base):
    "Singleton to stem off queries for instances"

    @classmethod
    def _all(cls):
        "Grab all AWS instances"
        return [
            i for r in get_connection().get_all_instances()
            for i in r.instances
        ]

    @classmethod
    def _create(cls, args, **kwargs):
        raise NotImplementedError("Coming Soon!")

    @classmethod
    def _delete(cls, args, **kwargs):
        raise NotImplementedError("Coming Soon!")


class security_groups(objects_base):
    "Singleton to stem off queries for security groups"

    @classmethod
    def _all(cls):
        "Grab all AWS Security Groups"
        return get_connection().get_all_security_groups()

    @classmethod
    def _create(cls, name, description, vpc_id=None, dry_run=False):
        return get_connection().create_security_group(
            name, description, vpc_id=vpc_id, dry_run=dry_run)

    @classmethod
    def _delete(cls, name=None, group_id=None, dry_run=False):
        return get_connection().delete_security_group(
            name=name, group_id=group_id, dry_run=dry_run)


class vpcs(objects_base):
    "Singleton to stem off queries for virtual private clouds"

    @classmethod
    def _all(cls):
        "Grab all AWS Virtual Private Clouds"
        return get_vpc_connection().get_all_vpcs()

    @classmethod
    def _create(cls, cidr_block, instance_tenancy=None, dry_run=False):
        "Create AWS Virtual Private Clouds"
        return get_vpc_connection().create_vpc(
            cidr_block, instance_tenancy=instance_tenancy, dry_run=dry_run)

    @classmethod
    def _delete(cls, id, dry_run=False):
        "Delete AWS Virtual Private Clouds"
        return get_vpc_connection().delete_vpc(id, dry_run=dry_run)
