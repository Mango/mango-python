"""
Mango Python Library Resources
"""
import pymango
from .client import req
from .error import InvalidApiKey


class Resource():
    """Mango Resource base class"""
    name = None

    def __init__(self):
        if not pymango.api_key:
            raise InvalidApiKey

    @classmethod
    def get_endpoint(cls):
        """
        Get API endpoint using the API version and the Resource name

        :return: String with endpoint, ex: v1/charges/
        """
        return "v{version}/{name}/".format(
            version=pymango.version,
            name=cls.name
        )


class GetableResource(Resource):
    @classmethod
    def get(cls, uid):
        """
        Return the resource representation

        :param uid: String with the UID of the resource
        :return: Dictionary with the resource representation
        """
        return req(pymango.api_key, "get", "{endpoint}{element}/".format(
            endpoint=cls.get_endpoint(),
            element=uid
        ))


class ListableResource(Resource):
    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of resources

        :param kwargs: Any optional argument accepted by the resource
        :return: List with a dictionary with the resource representation
        """
        return req(pymango.api_key, "get", cls.get_endpoint(), params=kwargs)


class ResourceCreatable(Resource):
    @classmethod
    def create(cls, **kwargs):
        """
        Create a Charge

        :param kwargs: Any optional argument accepted by the Charge resource
        :return: Dictionary with Charge representation
        """
        return req(pymango.api_key, "post", cls.get_endpoint(), kwargs)


class ResourceUpdatable(Resource):
    """Base class for updatable resources"""
    @classmethod
    def update(cls, uid, **kwargs):
        """
        Update resource

        :param uid: String with the UID of the resource
        :param kwargs: Any optional argument accepted by the resource
        :return: Dictionary with the resource representation
        """
        return req(pymango.api_key, "patch", "{endpoint}{element}/".format(
            endpoint=cls.get_endpoint(),
            element=uid
        ), data=kwargs)


class ResourceDeletable(Resource):
    """Base class for deletable resources"""
    @classmethod
    def delete(cls, uid):
        """
        Delete a resource

        :param uid: String with the UID of the resource
        :return: Dictionary with the resource representation
        """
        return req(pymango.api_key, "delete", "{endpoint}{element}/".format(
            endpoint=cls.get_endpoint(),
            element=uid
        ))


class ResourceDeletableAll(Resource):
    """Base class for delete entire collection of resources"""
    @classmethod
    def delete_all(cls):
        """
        Delete all resources from this collection

        :return: True if success, false otherwise.
        """
        return req(pymango.api_key, "delete", cls.get_endpoint())


class Charge(GetableResource, ListableResource, ResourceCreatable, Resource):
    """Mango Charge resource"""
    name = "charges"


class Refund(GetableResource, ListableResource, ResourceCreatable, Resource):
    """Mango Refund resource"""
    name = "refunds"


class Customer(GetableResource, ListableResource, ResourceCreatable, ResourceUpdatable, ResourceDeletable):
    """Mango Customer resource"""
    name = "customers"


class Card(GetableResource, ListableResource, ResourceCreatable, ResourceUpdatable, ResourceDeletable):
    """Mango Card resource"""
    name = "cards"


class Queue(GetableResource, ListableResource, ResourceDeletable, ResourceDeletableAll):
    """Mango Queue resource"""
    name = "queue"


class Installment(ListableResource, Resource):
    """Mango Installment resource"""
    name = "installments"


class Promotion(GetableResource, ListableResource, Resource):
    """Mango Promotion resource"""
    name = "promotions"


class Coupon(GetableResource, ListableResource, ResourceCreatable, ResourceUpdatable, Resource):
    """Mango Coupon resource"""
    name = "coupons"
