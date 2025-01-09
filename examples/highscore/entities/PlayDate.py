import datetime
from boto3.dynamodb.conditions import Key

try:
    from _factory import Entity
except ImportError:
    from ._factory import Entity

class PlayDate(Entity):
    """
    Entity representing a play whith the date as sort key
    """

    def __init__(self, username, date, **kwargs):
        super().__init__(username=username, **kwargs)
        # date gets some extra handling
        self._dateDt = date
        if not isinstance(date, datetime.datetime):
            self._dateDt = datetime.datetime.fromisoformat(date)
            # todo add tz if missing
        self.date = self._dateDt.isoformat()
    
    @property
    def pk(self):
        return self.username
    
    @property
    def sk(self):
        return "DATE#" + self.date
    
    ### Queries
    @classmethod
    def get_query_recent_plays(cls, username, limit):
        return dict(
            KeyConditionExpression=Key('pk').eq(username) & Key('sk').begins_with('DATE#'),
            ScanIndexForward=False, # desc order
            Limit=limit
        )
