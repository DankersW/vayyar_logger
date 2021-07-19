from boto3 import Session
from boto3.dynamodb.conditions import Key


class DbDriver:
    device_id = 'id_MzA6QUU6QTQ6RTQ6MDA6NTQ'

    def __init__(self, keys: dict, table: str):
        session = Session(
            aws_access_key_id=keys.get("aws_access_key"),  # named tuple settings
            aws_secret_access_key=keys.get("aws_secret_key"),
        )
        db = session.resource('dynamodb')
        self.db_table = db.Table(table)

    def query_db(self, oldest_timestamp, untill_timestamp=None):
        if untill_timestamp:
            query = Key('device_id').eq(self.device_id) & Key('timestamp').between(oldest_timestamp, untill_timestamp)
        else:
            query = Key('device_id').eq(self.device_id) & Key('timestamp').gte(oldest_timestamp)
        return self.db_table.query(KeyConditionExpression=query)['Items']

    def scan_db(self):
        return self.db_table.scan()['Items']
