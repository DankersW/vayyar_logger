import boto3
from boto3.dynamodb.conditions import Key
from yaml import safe_load
import time
import datetime


def query_db(oldest_timestamp, untill_timestamp=None):
    db = session.resource('dynamodb')
    db_table = db.Table('vayyar_home_c2c_room_status')
    if untill_timestamp:
        query = Key('device_id').eq('id_MzA6QUU6QTQ6RTQ6MDA6NTQ') & Key('timestamp').between(oldest_timestamp, untill_timestamp)
    else:
        #query = Key('device_id').eq('id_MzA6QUU6QTQ6RTQ6MDA6NTQ') & Key('timestamp').gte(oldest_timestamp)
        query = Key('device_id').eq('id_MzA6QUU6QTQ6RTQ6MDA6NTQ') & Key('timestamp').between(oldest_timestamp, 1626687473931)
    response = db_table.query(KeyConditionExpression=query)
    return response['Items']


with open("keys.yml") as config_file:
    config = safe_load(config_file)

session = boto3.Session(
    aws_access_key_id=config.get("aws_access_key"),  # named tuple settings
    aws_secret_access_key=config.get("aws_secret_key"),
)
#dynamodb = session.resource('dynamodb')
#table = dynamodb.Table('vayyar_home_c2c_room_status')
#resp = table.scan()
#data = resp['Items']

start_timestamp = round(time.time() * 1000)
start_timestamp = 1626686100002
timestamp_yesterday = start_timestamp - 86400000
live_data = query_db(oldest_timestamp=start_timestamp)
yesterday_data = query_db(oldest_timestamp=timestamp_yesterday, untill_timestamp=start_timestamp)

for i in live_data:
    print(i)
print("test")
for i in yesterday_data:
    print(i)

# dynamodb = boto3.resource('dynamodb', region_name='***')

# todo: query one day of data
# todo: query every item more than the start time
# todo: live plot
# todo: day plot

