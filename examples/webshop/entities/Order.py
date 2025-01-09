
from dynamodbEntities import Entity

class Order(Entity):

    def __init__(self, quantity, orderId, costs, orderDate, shippingStatus, itemId, userId, **kwargs):
        super().__init__(quantity=quantity, orderId=orderId, costs=costs, orderDate=orderDate, shippingStatus=shippingStatus, itemId=itemId, userId=userId, **kwargs)
    
    @property
    def pk(self):
        return self.userId
    
    @property
    def sk(self):
        return f"ORDER#{self.date}#{self.orderId}"

    @property
    def gsi_1(self):
        return self.shippingStatus
