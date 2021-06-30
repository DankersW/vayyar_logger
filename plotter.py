import boto3

session = boto3.Session(
    aws_access_key_id=AWS_SERVER_PUBLIC_KEY,  # named tuple settings
    aws_secret_access_key=AWS_SERVER_SECRET_KEY,
)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('vayyar_home_c2c_room_status')
resp = table.scan()
data = resp['Items']
print(data)
# dynamodb = boto3.resource('dynamodb', region_name='***')
