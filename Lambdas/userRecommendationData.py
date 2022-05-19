import json
import boto3

def lambda_handler(event, context):
    # TODO implement

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('userRecommendations')
    user_id ='xxxxxxxxxxxxxxxx'
    response = table.get_item(
        Key={
            'userId': user_id
        }
    )
    result=[]
    if 'Item' in response:
        result=response['Item']

        return {
            'statusCode': 200,
            'body': response['Item']

        }

    # print(response['Item'])

    return {
        'statusCode': 200,
        'body' : "No Data Found"
    }
