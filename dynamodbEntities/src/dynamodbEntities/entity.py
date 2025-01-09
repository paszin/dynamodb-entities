import datetime
try:
    from . import dynamodbHelpers
except ImportError:
    import dynamodbHelpers

from typing import Callable


def get_entity_class(**kwargs):
    """
    returns the entity class 
    """
    newEntity = Entity
    for k, v in kwargs.items():
        setattr(newEntity, k, v)
    return newEntity


class Entity:

    __reserved_names = ["_md", "_et"]
    __pk_name = "pk"
    __pk_type = "S"
    __sk_name = "sk"
    __sk_type = "S"
    __et_name = "_et"

    def __init__(self, **kwargs):

        for k, v in kwargs.items():
            try:
                setattr(self, k, v)
            except AttributeError:
                # ignore pk, sk, and gsi_1 as they don't have a setter attribute
                continue

    @property
    def __md(self):
        return datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    @property
    def _md(self):
        return self.__md

    @property
    def __et(self):
        return self.__class__.__name__

    @property
    def _et(self):
        return self.__et

    def __repr__(self):
        s = self.pk
        try:
            s += " " + self.sk
        except:
            pass
        return s

    def as_item(self, marshall=False):
        """
        returns a dictionary of the entity's
        """
        item = {name: getattr(self, name) for name in dir(self) if not name.startswith(
            "_") and not isinstance(getattr(self, name), Callable) or name in Entity.__reserved_names}
        if marshall:
            item = dynamodbHelpers.dumps(item, as_dict=True)
        return item

    def get_key(self, marshall=False):
        """
        returns a dict with primary key and sort key (if given)
        if marhsall is True, the dict will be marshalled (using the __pk_type and __sk_type)
        """
        if marshall:
            resp = {self.__pk_name: {self.__pk_type: self.pk}}
            if self.__sk_name is not None:
                resp[self.__sk_name] = {self.__sk_type: self.sk}
            return resp
        resp = {self.__pk_name: self.pk}
        if self.__sk_name is not None:
            resp[self.__sk_name] = self.sk
        return resp

    def _get_extended_expression_attribute_names(self, existing_names):
        d = {f"#{name}": name for name in self.__reserved_names}
        d.update(existing_names)
        return d

    def _get_expression_attribute_names(self):
        return {f"#{name}": name for name in self.as_item()}

    def _get_extended_expression_attribute_values(self, existing_values):
        d = {f":{name}": getattr(self, name) for name in self.__reserved_names}
        d.update(existing_values)
        return d

    def _get_expression_attribute_values(self):
        return dynamodbHelpers.dumps({f":{name}": value for name, value in self.as_item().items()})

    def _get_update_expression(self):
        return "SET " + " ".join([f"#{name} = :{name}" for name in self.as_item()])

    def _get_extended_update_expression(self):
        return ", " + ", ".join([f"#{name} = :{name}" for name in self.__reserved_names])

    def get_put(self):
        return {
            "Key": self._get_key(),
            "UpdateExpression": self._get_update_expression(),
            "ExpressionAttributeNames": self._get_expression_attribute_names(),
            "ExpressionAttributeValues": self._get_expression_attribute_values(),
        }


if __name__ == "__main__":
    pass
