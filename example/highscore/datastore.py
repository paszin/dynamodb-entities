

from dynamodbEntities import BaseDatastore
from dynamodbEntities.decorators import add_convert_param
from dynamodbEntities.helpers import get_default_lookup

try:
    from .entities import PlayDate, PlayScore, UserStats
    from . import entities
except ImportError:
    from entities import PlayDate, PlayScore, UserStats
    import entities

lookup = get_default_lookup(entities)

class Datastore(BaseDatastore):

    def add_play(self, username, date, points):
        with self.table.batch_writer() as writer:
            writer.put_item(Item=PlayDate(
                username, date.isoformat(), points=points).as_item()),
            writer.put_item(Item=PlayScore(username, points,
                            date=date.isoformat()).as_item())
        self.table.update_item(
            **UserStats(username).get_play_counter_increment())

    @add_convert_param(lookup)
    def get_highscore(self, limit=10, **kwargs):
        resp = self.table.query(**PlayScore.get_query_top_results(limit))
        return resp

    @add_convert_param(lookup)
    def get_recent_plays(self, username, limit=10, **kwargs):
        resp = self.table.query(
            **PlayDate.get_query_recent_plays(username, limit))
        return resp

    @add_convert_param(lookup)
    def get_user_highscore(self, username, limit=10, **kwargs):
        resp = self.table.query(
            **PlayScore.get_query_user_top_results(username, limit))
        return resp

    @add_convert_param(lookup)
    def get_user_stats(self, username, **kwargs):
        resp = self.table.get_item(**UserStats.get_user_stats(username))
        return resp

