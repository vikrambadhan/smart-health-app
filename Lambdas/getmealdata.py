import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # TODO implement
    # print(event['mealId']);
    mealId = event['mealId']

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('mealplans')
    dynamoDBResponses = []
    dynamoDBResponses.append(table.query(KeyConditionExpression=Key('meal_id').eq(mealId)))


    # print(dynamoDBResponses[0]['Items'])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'mealInfo': dynamoDBResponses[0]['Items']
    }
