
import boto3


class BaseDatastore:

    def __init__(self, table=None, table_name=None, client=None, session=None, endpoint_url=None):

        if table:
            self.table = table

        if session:
            self.session = session
            self.client = session.client('dynamodb', endpoint_url=endpoint_url)
            self.resource = session.resource(
                'dynamodb', endpoint_url=endpoint_url)
            self.table = self.resource.Table(table_name)
