"""
ec2.models.managers
~~~~~~~~

:copyright: (c) 2014 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""

from .base import objects_base
from ec2.connection import get_connection, get_vpc_connection


class BaseManager(objects_base):
    """ """
    @classmethod
    def _all(cls, args, **kwargs):
        raise NotImplementedError("Coming Soon!")

    @classmethod
    def _create(cls, args, **kwargs):
        raise NotImplementedError("Coming Soon!")

    @classmethod
    def _delete(cls, args, **kwargs):
        raise NotImplementedError("Coming Soon!")


class InstanceManager(BaseManager):
    """ """
    @classmethod
    def _all(cls):
        "Grab all AWS instances"
        reservations = get_connection().get_all_instances()
        instances = [i for r in reservations for i in r.instances]
        return instances


class ReservationManager(BaseManager):
    """ """

    @classmethod
    def _all(cls):
        "Grab all AWS reservations"
        reservations = get_connection().get_all_reservations()
        return reservations


class SecurityGroupManager(BaseManager):
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


class VPCManager(BaseManager):
    """ """
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
