
try:
    from _factory import Entity
except ImportError:
    from ._factory import Entity

class UserStats(Entity):

    def __init__(self, username, **kwargs):
        self.playCount = None
        super().__init__(username=username, **kwargs)

    @property
    def pk(self):
        return self.username
    
    @property
    def sk(self):
        return "STATS"
    
    def get_play_counter_increment(self):
        return dict(
            Key=self._get_key(),
            ExpressionAttributeValues=self._get_extended_expression_attribute_values({":inc": 1, ":start": 0, ":username": self.username}),
            UpdateExpression="SET #counter = if_not_exists(#counter, :start) + :inc, #username = :username" + self._get_extended_update_expression(),
            ExpressionAttributeNames=self._get_extended_expression_attribute_names({
                '#counter': 'playCount',  # Attribute name
                "#username": "username"
            })
        )
    
    @classmethod
    def get_user_stats(cls, username):
        return dict(
            Key=cls(username)._get_key()
        )
