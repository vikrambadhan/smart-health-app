import json
import hashlib
import boto3
import base64
#from botocore.vendored import requests
import requests
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    # TODO implement
    print(event)
    user_id = event['user_id']
    print('user_id')
    print(user_id)
    code=user_id
    redirect_uri='https://mealdeliveryapp.s3.amazonaws.com/Resources/HTML/dashboard.html'
    client_id='xxxxxxxxx'
    client_secret='xxxxxxxxxxxxxxx'

    token_url=f"https://xxxxxxxxx.auth.us-east-1.amazoncognito.com/oauth2/token"
    message = bytes(f"{client_id}:{client_secret}",'utf-8')
    secret_hash = base64.b64encode(message).decode()
    payload = {
        "grant_type": 'authorization_code',
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Authorization": f"Basic {secret_hash}"}

    resp = requests.post(token_url, params=payload, headers=headers)
    reponsejson = resp.json();
    print('token response')
    print(reponsejson)

    if 'access_token' in resp.json():
        access_token=reponsejson['access_token'];
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload={}
        url = 'https://xxxxxxxxx.auth.us-east-1.amazoncognito.com/oauth2/userInfo'
        r = requests.get(url, data=json.dumps(payload), headers=headers)
        print('Auth response')
        print(r.json())
        if 'email' in r.json():
            email = r.json()['email']
        else:
            return {
                'statusCode': 200,
                'headers':{
                    'Access-Control-Allow-Origin':'*',
                    'Access-Control-Allow-Credentials':True
                },
                'body': json.dumps({
                    'invalid_access_token':'1'
                })
            }
        print(email)
        em = email.split('@')[0]
        em1 = email.split('@')[1].split('.')
        m = hashlib.md5()
        m.update(em.encode('utf8'))
        m.update(em1[0].encode('utf8')+em1[1].encode('utf8'))
        print(m.hexdigest())
        user_id = m.hexdigest()
        print('deduced user_id')
        print(user_id)
        item = check_user_profile(user_id)
        if not item:
            print('no item found for user_id')
            add_active_user(user_id)
            #put_user_profile(user_id, '0', email)
            # send_email(email)
            print('user_profile found')
        ##############
        return {
            'statusCode': 200,
            'headers':{
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Credentials':True
            },
            'body': json.dumps({
                'found_access_token':'1',
                'access_token':access_token,
                'user_id':user_id
            })
        }
    else:
        user_id=code;
        return {
            'statusCode': 200,
            'headers':{
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Credentials':True
            },
            'body': json.dumps({
                'user_id':user_id
            }, cls=DecimalEncoder)
        }
    #if 'queryStringParameters' in event:
    #    access_token = event['queryStringParameters']['user_id']
    #    print('access_token received')
    #else:
    #    access_token = "accessToken"




def check_user_profile(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_active')
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    if 'Item' in response:
        item = response['Item']
        print("Get active user succeeded:")
        print(item)
        return item
    # print(json.dumps(response, indent=4))
    return None


def put_user_profile(user_id, completion_level, email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    response = table.put_item(
        Item={
            'user_id' : user_id,
            'completion_level': completion_level,
            'email': email
        }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4))


def add_active_user(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_active')
    response = table.scan()
    print(response)
    if response['Count'] != 0:
        delete_active_user(response['Items'])
    response = table.put_item(
        Item={
            'user_id':user_id

        })
    print(response)

def delete_active_user(items):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_active')
    print(items)
    for item in items:
        response = table.delete_item(
            Key={
                'user_id': item['user_id']
            }
        )
        print(response)

def send_email(email):
    client = boto3.client('ses',
                          aws_access_key_id='KeyValue',
                          aws_secret_access_key='SecretValue')
    response = client.send_email(
        Source='xxxxxxxxxxx@gmail.com',
        Destination={
            'ToAddresses': [
                email,
            ]
        },
        Message={
            'Subject': {
                'Data': 'MyMacroChef'
            },
            'Body': {
                'Text': {
                    'Data': 'Welcome to MyMacroChef\n Please fill out your profile to achieve maximum rewards.!!!'
                }
            }
        }
    )
    print(response)
