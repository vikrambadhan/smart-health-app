import json
import boto3
from datetime import datetime
import hashlib
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from decimal import Decimal

def lambda_handler(event, context):
    # TODO implement
    print(event)
    user_id = event['user_id']
    user_details = check_user(user_id)
    userName=event["userName"]
    age=event["age"]
    gender=event["gender"]
    ethnicity=event["ethnicity"]
    height=event["height"]
    weight=event["weight"]
    #targetWeight=event["targetWeight"]
    activity=event["activity"]
    medicalCondition=event["medicalCondition"]
    dietaryPreference=event["dietaryPreference"]
    mealpreference=event["mealpreference"]
    allergies=event["allergies"]
    #cuisine=event["cuisine"]
    street=event["street"]
    city=event["city"]
    user_state=event["user_state"]
    phoneNo=event["phoneNo"]
    heightF=Decimal(height)
    weightF=Decimal(weight)
    bmi = weightF/(heightF/100)**2
    bmi = "{:.2f}".format(bmi)
    event["bmi"]=str(bmi)
    intage = int(age)
    #calories
    if(gender=='female'):
        if(intage>=2 and intage<=3):
            if(activity=='na'):
                calories=1000
            elif(activity=='sa'):
                calories=1200
            elif(activity=='ma'):
                calories=1300
            else:
                calories=1400
        elif (intage>=4 and intage<=8):
            if(activity=='na'):
                calories=1200
            elif(activity=='sa'):
                calories=1400
            elif(activity=='ma'):
                calories=1500
            else:
                calories=1800
        elif (intage>=9 and intage<=13):
            if(activity=='na'):
                calories=1600
            elif(activity=='sa'):
                calories=1900
            elif(activity=='ma'):
                calories=2000
            else:
                calories=2200
        elif (intage>=14 and intage<=18):
            if(activity=='na'):
                calories=1800
            elif(activity=='sa'):
                calories=2100
            elif(activity=='ma'):
                calories=2200
            else:
                calories=2400
        elif (intage>=19 and intage<=30):
            if(activity=='na'):
                calories=2000
            elif(activity=='sa'):
                calories=2200
            elif(activity=='ma'):
                calories=2300
            else:
                calories=2400
        elif (intage>=31 and intage<=50):
            if(activity=='na'):
                calories=1800
            elif(activity=='sa'):
                calories=2000
            elif(activity=='ma'):
                calories=2100
            else:
                calories=2200
        else:
            if(activity=='na'):
                calories=1600
            elif(activity=='sa'):
                calories=1900
            elif(activity=='ma'):
                calories=2000
            else:
                calories=2200
    else:
        if(intage>=2 and intage<=3):
            if(activity=='na'):
                calories=1000
            elif(activity=='sa'):
                calories=1200
            elif(activity=='ma'):
                calories=1300
            else:
                calories=1400
        elif (intage>=4 and intage<=8):
            if(activity=='na'):
                calories=1400
            elif(activity=='sa'):
                calories=1700
            elif(activity=='ma'):
                calories=1800
            else:
                calories=2000
        elif (intage>=9 and intage<=13):
            if(activity=='na'):
                calories=1800
            elif(activity=='sa'):
                calories=2200
            elif(activity=='ma'):
                calories=2400
            else:
                calories=2600
        elif (intage>=14 and intage<=18):
            if(activity=='na'):
                calories=2200
            elif(activity=='sa'):
                calories=2700
            elif(activity=='ma'):
                calories=3000
            else:
                calories=3200
        elif (intage>=19 and intage<=30):
            if(activity=='na'):
                calories=2400
            elif(activity=='sa'):
                calories=2700
            elif(activity=='ma'):
                calories=2800
            else:
                calories=3000
        elif (intage>=31 and intage<=50):
            if(activity=='na'):
                calories=2200
            elif(activity=='sa'):
                calories=2600
            elif(activity=='ma'):
                calories=2800
            else:
                calories=3000
        else:
            if(activity=='na'):
                calories=2000
            elif(activity=='sa'):
                calories=2400
            elif(activity=='ma'):
                calories=2600
            else:
                calories=2800

    if(user_details):
        print("Found User profile")
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('user_profile')
        table2response = table.update_item(Key={'user_id': user_id},
                                           UpdateExpression="set userName=:userName, age=:age, gender=:gender, ethnicity=:ethnicity, height=:height, weight=:weight, activity=:activity, medicalCondition=:medicalCondition, dietaryPreference=:dietaryPreference,mealpreference=:mealpreference, allergies=:allergies, bmi=:bmi, calories=:calories, street=:street, city=:city, user_state=:user_state, phoneNo=:phoneNo",
                                           ExpressionAttributeValues={':userName': userName,':age': age,':gender': gender,':ethnicity': ethnicity,':height': height,':weight': weight,':activity': activity,':medicalCondition': medicalCondition,':dietaryPreference': dietaryPreference,':mealpreference':mealpreference,':allergies': allergies,':bmi':bmi,':calories':calories,':street':street,':city':city,':user_state':user_state,':phoneNo':phoneNo},ReturnValues="UPDATED_NEW")
    else:
        print("No User profile found. Creating new.")
        put_user_profile(user_id,userName,age,gender,ethnicity,height,weight,
                         activity,medicalCondition,dietaryPreference,mealpreference,allergies,
                         bmi, calories, street,city,user_state,phoneNo)
        #send_notification(first_name,last_name,phone)
        #send_email(email)
    return {
        'statusCode': 200,
        'body': json.dumps('user profile added')
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

def put_user_profile(user_id,userName,age,gender,ethnicity,height,weight,
                     activity,medicalCondition,dietaryPreference,mealpreference,allergies,
                     bmi, calories, street,city,user_state,phoneNo):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    response = table.put_item(
        Item={
            'user_id' : user_id,
            'userName':userName,
            'age' : age,
            'gender' : gender,
            'ethnicity' : ethnicity,
            'height' : height,
            'weight': weight,
            'activity' : activity,
            'medicalCondition' : medicalCondition,
            'dietaryPreference' : dietaryPreference,
            'mealpreference':mealpreference,
            'allergies': allergies,
            'bmi': bmi,
            'calories': calories,
            'street': street,
            'city': city,
            'user_state': user_state,
            'phoneNo': phoneNo
        }
    )
    print("PutItem succeeded:")
    print(response)

def send_notification(first_name,last_name,phone):
    sns = boto3.client('sns',
                       aws_access_key_id='accessKey',
                       aws_secret_access_key='secretKey')
    response = sns.publish(PhoneNumber='+1'+phone,
                           Message='Welcome '+first_name+' '+last_name+' to MyMacroChef, you will be further notified on this number.')
    print(response)

def send_email(first_name,last_name,email):
    client = boto3.client('ses',
                          aws_access_key_id='accessKey',
                          aws_secret_access_key='secretKey')
    response = client.send_email(
        Source='sourceEmailId',
        Destination={
            'ToAddresses': [
                email,
            ]
        },
        Message={
            'Subject': {
                'Data': 'MyMacroChef Sign Up Completion'
            },
            'Body': {
                'Text': {
                    'Data': 'Welcome '+first_name+' '+last_name+' to MyMacroChef\nYou will be further notified on this email'
                }
            }
        }
    )
    print(response)
