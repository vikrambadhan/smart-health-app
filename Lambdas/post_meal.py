import json

def lambda_handler(event, context):
    print(event)
    user_id = event['user_id']
    meal_id = event['mealid']
    user_profile = check_user(user_id)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def check_user(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    if 'Item' in response:
        print("GetItem succeeded:")
        return response['Item']
    return False
