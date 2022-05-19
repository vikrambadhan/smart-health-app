import json
import uuid
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # print(event['mealId']);
    # print(event['orderDate']);
    # print(event['userId']);

    orderId = str(uuid.uuid4())
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('orders')

    table.put_item(Item={
        'orderId': orderId,
        'mealId':event['mealId'] ,
        'orderDate':date_time,
        'userId':event['userId'],
        'orderAmount': event['orderAmount'],
        'frequency': event['frequency'],
        'street' : event['street'],
        'city' : event['city'],
        'state' : event['state'],
        'country' : event['country'],
        'zip' : event['zip']
    })

    # TODO implement
    return {
        'statusCode': 200,
        'orderId': orderId
    }
