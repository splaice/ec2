"""
ec2.models.models
~~~~~~~~

:copyright: (c) 2014 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""

from boto.ec2.instance import Reservation as OrigReservation
from boto.ec2.instance import Instance as OrigInstance
from boto.ec2.securitygroup import SecurityGroup as OrigSecurityGroup
from boto.vpc.vpc import VPC as OrigVPC

from .managers import (
    InstanceManager,
    ReservationManager,
    SecurityGroupManager,
    VPCManager)


class DeleteMixin(object):
    def delete(self, *args, **kwargs):
        self.objects.clear()
        super(DeleteMixin, self).delete()


class Instance(DeleteMixin, OrigInstance):
    objects = InstanceManager()


class Reservation(DeleteMixin, OrigReservation):
    objects = ReservationManager()

    def delete(self, *args, **kwargs):
        self.objects.clear()
        reservation = self.objects.get(id=self.id)
        instances = [i for i in reservation.instances]
        self.objects.delete([i.id for i in instances])

    def stop(self, *args, **kwargs):
        self.objects.clear()
        reservation = self.objects.get(id=self.id)
        instances = [i for i in reservation.instances]
        self.objects.stop([i.id for i in instances])


class SecurityGroup(DeleteMixin, OrigSecurityGroup):
    objects = SecurityGroupManager()


class VPC(DeleteMixin, OrigVPC):
    objects = VPCManager()
