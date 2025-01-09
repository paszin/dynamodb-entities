
from dynamodbEntities import Entity

class Customer(Entity):

    def __init__(self, name, address, hasNewsletterSubscription, email, **kwargs):
        super().__init__(name=name, address=address, hasNewsletterSubscription=hasNewsletterSubscription, email=email, **kwargs)
    
    @property
    def pk(self):
        return self.email
    
    @property
    def sk(self):
        return "PROFILE"

