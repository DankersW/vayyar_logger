import boto3
from boto3.dynamodb.conditions import Key
from yaml import safe_load
import time

#from matplotlib import pyplot


class DbDriver:
    def __init__(self, table: str):
        session = boto3.Session(
            aws_access_key_id=config.get("aws_access_key"),  # named tuple settings
            aws_secret_access_key=config.get("aws_secret_key"),
        )
        db = session.resource('dynamodb')
        self.db_table = db.Table(table)

    def query_db(self, oldest_timestamp, untill_timestamp=None):
        if untill_timestamp:
            query = Key('device_id').eq('id_MzA6QUU6QTQ6RTQ6MDA6NTQ') & Key('timestamp').between(oldest_timestamp,
                                                                                                 untill_timestamp)
        else:
            # query = Key('device_id').eq('id_MzA6QUU6QTQ6RTQ6MDA6NTQ') & Key('timestamp').gte(oldest_timestamp)
            query = Key('device_id').eq('id_MzA6QUU6QTQ6RTQ6MDA6NTQ') & Key('timestamp').between(oldest_timestamp,
                                                                                                 1626687473931)
        return self.db_table.query(KeyConditionExpression=query)['Items']

    def scan_db(self):
        return self.db_table.scan()['Items']



with open("keys.yml") as config_file:
    config = safe_load(config_file)

start_timestamp = round(time.time() * 1000)
start_timestamp = 1626686100002
timestamp_yesterday = start_timestamp - 86400000

db = DbDriver(table='vayyar_home_c2c_room_status')

live_data = db.query_db(oldest_timestamp=start_timestamp)
yesterday_data = db.query_db(oldest_timestamp=timestamp_yesterday, untill_timestamp=start_timestamp)

for i in live_data:
    print(i)
print("test")
for i in yesterday_data:
    print(i)

# dynamodb = boto3.resource('dynamodb', region_name='***')

# todo: live plot
# todo: day plot

