import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    print("Logged event is : ")
    print(event)

    orderId = event['orderId']

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    ordersTable = dynamodb.Table('orders')

    dynamoDBResponsesOrders = []
    dynamoDBResponsesOrders.append(ordersTable.query(KeyConditionExpression=Key('orderId').eq(orderId)))

    table = dynamodb.Table('mealplans')
    mealId = dynamoDBResponsesOrders[0]['Items'][0]['mealId']
    dynamoDBResponses = []
    dynamoDBResponses.append(table.query(KeyConditionExpression=Key('meal_id').eq(mealId)))


    # TODO implement
    return {
        'statusCode': 200,
        'orderInfo':dynamoDBResponsesOrders[0]['Items']
        ,'mealInfo': dynamoDBResponses[0]['Items'],
    }
