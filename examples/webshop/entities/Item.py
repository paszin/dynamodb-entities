
from dynamodbEntities import Entity


class Item(Entity):

    def __init__(self, itemId, name, price, description, quantity, **kwargs):
        super().__init__(itemId=itemId, name=name, price=price,
                         description=description, quantity=quantity, **kwargs)

    @property
    def pk(self):
        return "ITEM"

    @property
    def sk(self):
        return self.itemId

    @classmethod
    def get_query_all_items(cls):
        return dict(
            Key={"pk": "ITEM"},
        )
