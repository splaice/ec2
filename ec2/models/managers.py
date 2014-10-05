"""
ec2.models.managers
~~~~~~~~

:copyright: (c) 2014 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""

from datetime import datetime, timedelta
from ec2.connection import get_connection, get_vpc_connection

from .helpers import make_compare


MAX_CACHE_AGE = 60 * 5


class _EC2MetaClass(type):
    "Metaclass for all EC2 filter type classes"

    def __new__(cls, name, bases, attrs):
        # Append MultipleObjectsReturned and DoesNotExist exceptions
        for contrib in ('MultipleObjectsReturned', 'DoesNotExist'):
            attrs[contrib] = type(contrib, (Exception,), {})
        return super(_EC2MetaClass, cls).__new__(cls, name, bases, attrs)


class BaseManager(object):
    "Base class for all EC2 filter type classes"

    __metaclass__ = _EC2MetaClass

    @classmethod
    def is_cache_expired(cls):
        if hasattr(cls, '_cached_at'):
            if datetime.utcnow() - cls._cached_at > timedelta(seconds=MAX_CACHE_AGE):
                return True

        return False

    @classmethod
    def all(cls):
        """
        Wrapper around _all() to cache and return all results of something

        >>> ec2.instances.all()
        [ ... ]
        """
        if not hasattr(cls, '_cache') or cls.is_cache_expired():
            cls._cache = cls._all()
            cls._cached_at = datetime.utcnow()
        return cls._cache

    @classmethod
    def get(cls, **kwargs):
        """
        Generic get() for one item only

        >>> ec2.instances.get(name='production-web-01')
        <Instance: ...>
        """
        things = cls.filter(**kwargs)
        if len(things) > 1:
            # Raise an exception if more than one object is matched
            raise cls.MultipleObjectsReturned
        elif len(things) == 0:
            # Rase an exception if no objects were matched
            raise cls.DoesNotExist
        return things[0]

    @classmethod
    def filter(cls, **kwargs):
        """
        The meat. Filtering using Django model style syntax.

        All kwargs are translated into attributes on the underlying objects.
        If the attribute is not found, it looks for a similar key
        in the tags.

        There are a couple comparisons to check against as well:
            exact: check strict equality
            iexact: case insensitive exact
            like: check against regular expression
            ilike: case insensitive like
            contains: check if string is found with attribute
            icontains: case insensitive contains
            startswith: check if attribute value starts with the string
            istartswith: case insensitive startswith
            endswith: check if attribute value ends with the string
            iendswith: case insensitive startswith
            isnull: check if the attribute does not exist

        >>> ec2.instances.filter(name__startswith='production')
        [ ... ]
        """
        qs = cls.all()
        for key in kwargs:
            qs = filter(lambda i: make_compare(key, kwargs[key], i), qs)
        return qs

    @classmethod
    def clear(cls):
        "Clear the cached instances"
        try:
            del cls._cache
        except AttributeError:
            pass


class CreateManagerMixin(object):
    @classmethod
    def create(cls, *args, **kwargs):
        """
        Generic create()

        >>> ec2.vpcs.create('10.10.10.0/16')
        <VPC: ...>
        """
        result = cls._create(*args, **kwargs)
        cls.clear()
        return result


class DeleteManagerMixin(object):
    @classmethod
    def delete(cls, *args, **kwargs):
        """
        Generic delete()

        >>> ec2.vpcs.delete('vpc-123')
        True
        """
        result = cls._delete(*args, **kwargs)
        cls.clear()
        return result


class InstanceManager(BaseManager, CreateManagerMixin, DeleteManagerMixin):
    """ """
    @classmethod
    def _all(cls):
        "Grab all AWS instances"
        reservations = get_connection().get_all_instances()
        instances = [i for r in reservations for i in r.instances]
        return instances

    @classmethod
    def _create(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def _delete(cls, *args, **kwargs):
        raise NotImplementedError()


class ReservationManager(BaseManager):
    """ """

    @classmethod
    def _all(cls):
        "Grab all AWS reservations"
        reservations = get_connection().get_all_reservations()
        return reservations


class SecurityGroupManager(BaseManager, CreateManagerMixin, DeleteManagerMixin):
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


class VPCManager(BaseManager, CreateManagerMixin, DeleteManagerMixin):
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
