
import math
from boto3.dynamodb.conditions import Key

try:
    from _factory import Entity
except ImportError:
    from ._factory import Entity

class PlayScore(Entity):
    """
    Entity representing a play with the score as sort key
    """

    __MAX_POINTS = 1000
    __MAX_DIGITS = math.ceil(math.log10(__MAX_POINTS)) + 1

    def __init__(self, username, points, **kwargs):
        super().__init__(username=username, **kwargs)
        points = min(self.__MAX_POINTS, points)
        self.points = points
    
    @property
    def pk(self):
        return self.username
    
    @property
    def sk(self):
        return "SCORE#" + str(self.points).zfill(self.__MAX_DIGITS)
    
    @property
    def gsi_1(self):
        return "SCORE"
    
    @classmethod
    def get_query_top_results(cls, limit):
        return dict(
            IndexName='gsi_1',
            KeyConditionExpression=Key('gsi_1').eq('SCORE'),
            ScanIndexForward=False, # desc order
            Limit=limit
        )
    
    @classmethod
    def get_query_user_top_results(cls, username, limit):
        return dict(
            KeyConditionExpression=Key('pk').eq(username) & Key('sk').begins_with('SCORE#'),
            ScanIndexForward=False, # desc order
            Limit=limit
        )
