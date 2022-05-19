import json
import uuid
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # print(event['mealId']);
    # print(event['orderDate']);
    # print(event['userId']);

    paymentId = str(uuid.uuid4())
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('payments')

    table.put_item(Item={
        'paymentId': paymentId,
        'orderId':event['orderId'] ,
        'paymentDate':date_time
    })

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='orderConfirmationMessages')
    # queue_message = {"orderId": event['orderId']}
    response = queue.send_message(MessageBody=event['orderId'])

    # TODO implement
    return {
        'statusCode': 200,
        'orderId': paymentId
    }
