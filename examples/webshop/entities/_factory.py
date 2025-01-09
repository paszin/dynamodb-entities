
"""
This factory file is used to create a customized Entity class.
Import this new Entity.
"""


from dynamodbEntities.entity import get_entity_class

Entity = get_entity_class(
    # name of the partition key
    __pk_name="pk",
    # type of the partition key in the DynamoDB format, use "S" for string, "N" for number
    __pk_type="S",
    # name of the sort key
    __sk_name="sk",
    # type of the sort key in the DynamoDB format, use "S" for string, "N" for number
    __sk_type="S",
     # name of the entity property,
    __et_name = "_et",
)


# Use the code below to further overwrite the Entity class
'''
class Entity(Entity):

    __reserved_names = ["modified_date", "entity"]

    @property
    def modified_date(self):
        """
        a custom last modified date
        """
        # Implement a custom last modified date here, or return the default
        return self.__md

    @property
    def entity(self):
        """
        a custom entity property
        """
        return self.__et
 
'''
