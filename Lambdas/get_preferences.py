import os
import io
import boto3
import json
import csv
import hashlib

def lambda_handler(event, context):
    print(event)
    user_id=event["user_id"]
    userName=event["userName"]
    age=event["age"]
    gender=event["gender"]
    ethnicity=event["ethnicity"]
    height=event["height"]
    weight=event["weight"]
    targetWeight=event["targetWeight"]
    activity=event["activity"]
    medicalCondition=event["medicalCondition"]
    dietaryPreference=event["dietaryPreference"]
    allergies=event["allergies"]
    cuisine=event["cuisine"]
    heightF=float(height)
    weightF=float(weight)
    bmi = weightF/(heightF/100)**2
    event["bmi"]=str(bmi)
    user_profile = check_user_profile(user_id)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    if(user_profile):
        print("Found User profile")
        table2response = table.update_item(Key={'user_id': user_id},
                                           UpdateExpression="set userName=:userName, age=:age, gender=:gender, ethnicity=:ethnicity, height=:height, weight=:weight, targetWeight=:targetWeight, activity=:activity, medicalCondition=:medicalCondition, dietaryPreference=:dietaryPreference, allergies=:allergies, cuisine=:cuisine, bmi:bmi",
                                           ExpressionAttributeValues={':userName': userName,':age': age,':gender': gender,':ethnicity': ethnicity,':height': height,':weight': weight,':targetWeight': targetWeight,':activity': activity,':medicalCondition': medicalCondition,':dietaryPreference': dietaryPreference,':allergies': allergies,':cuisine': cuisine,':bmi':bmi},ReturnValues="UPDATED_NEW")
    else:
        print("No User profile found. Creating new.")
        table2response = table.put_item(Item=event)

    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Credentials':True
        },
        'body': json.dumps({
            'user_id':"yashika",
            'page_num':10,
            'selection': []
        })
    }

def check_user_profile(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    if 'Item' in response:
        item = response['Item']
        print("Get profile succeeded:")
        print(item)
        return item
    return None
