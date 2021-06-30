import boto3
from yaml import safe_load

with open("keys.yml") as config_file:
    config = safe_load(config_file)

session = boto3.Session(
    aws_access_key_id=config.get("aws_access_key"),  # named tuple settings
    aws_secret_access_key=config.get("aws_secret_key"),
)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('vayyar_home_c2c_room_status')
resp = table.scan()
data = resp['Items']
print(data)
# dynamodb = boto3.resource('dynamodb', region_name='***')
