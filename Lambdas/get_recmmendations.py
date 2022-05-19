import os
import io
import boto3
import json
import csv
import pandas as pd
import numpy as np
import hashlib
from boto3.dynamodb.conditions import Key, Attr

# grab environment variables

runtime= boto3.client('runtime.sagemaker',
                      aws_access_key_id='xxxxxxxxxxx',
                      aws_secret_access_key='xxxxxxxxxxxxxxxx')



s3 = boto3.client('s3')
def lambda_handler(event, context):
    print(event)

    # userId = '60a6c4a9dc6bccacad0254eaeb340410' #Get this from the event
    user_profile = check_user_profile(user_id)
    if not user_profile:
        return {
            'statusCode': 200,
            'headers':{
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Credentials':True
            },
            'body': json.dumps('user not found')
        }



    # age = str(user_profile['age'])
    # sex = str(user_profile['gender'])
    # weight = str(user_profile['weight'])
    # height = str(user_profile['height'])
    # calorie_intake = str(user_profile['calories'])
    # activity = str(user_profile['activity'])

    # # print("Received event: " + json.dumps(event, indent=2))

    # # data = json.loads(json.dumps(event))
    #sex,age,weight,height,calorie_intake, activity = 1.00e+00, 2.70e+01, 1.35e+02, 1.53e+02, 1.90e+03, 2.00e+00
    # payload = "1.00e+00, 2.70e+01, 1.35e+02, 1.53e+02, 1.90e+03,2.00e+00"

    #payload = sex + ',' + age + ',' + weight + ',' + height + ',' + calorie_intake + ',' +  activity
    #print(payload)

    # response = runtime.invoke_endpoint(EndpointName='kmeans-2022-05-13-21-44-28-285',
    #                                   ContentType='text/csv',
    #                                   Body=payload)
    # print("OUTPUT OF MY KMEANS IS :")
    # print(response)
    # result = json.loads(response['Body'].read().decode())
    # print(result)

    # result = {'predictions': [{'distance_to_cluster': 31.28098487854004, 'closest_cluster': 4.0}]}

    clusterfile = s3.get_object(Bucket='mealdeliveryapp', Key='Resources/Kmeansoutput/kmeans_output_users_cluster.csv')
    clusterDF = pd.read_csv(clusterfile['Body'])

    outputfile = s3.get_object(Bucket='mealdeliveryapp', Key='Resources/Kmeansoutput/output_cal.csv')
    outputDF = pd.read_csv(outputfile['Body'])

    #print(clusterDF)
    #print(clusterDF['calorie_intake'][0])

    daily_intake_cal = clusterDF['calorie_intake'][0]/3
    #print(daily_intake_cal)

    outputDF = outputDF[outputDF['calories'] < daily_intake_cal]
    #print(outputDF)

    pref = user_profile['dietaryPreference']
    #print(pref)

    mandatory = ''
    optional = ''

    if pref is not None or pref !='':
        if(pref == 'nonvegetarian'):
            mandatory = 'whitemeat'
        elif(pref == 'vegetarian'):
            mandatory = 'vegan,milk'
        elif(pref == 'vegan'):
            mandatory = 'vegan'
        else:
            mandatory = 'egg'

        #mandatory_preferences = 'egg,fish,whitemeat'.split(',')
        diet_preferences = mandatory.split(',')
        diet_preferences_df = outputDF[outputDF[diet_preferences].sum(axis=1) ==len(diet_preferences)].copy()
        #temp[optional_preferences].sample(5)

    else:

        diet_preferences_df = outputDF.sample(4)





    meal_pref = user_profile['mealpreference']
    if meal_pref is not None or meal_pref !='':
        meal_pref2 = meal_pref.split(',')
        while("" in meal_pref2) :
            meal_pref2.remove("")
        meal_pref2_preferences = meal_pref2
        meal_pref2_preferences_df = outputDF[outputDF[meal_pref2_preferences].sum(axis=1) ==len(meal_pref2_preferences)].copy()
    else:
        meal_pref2_preferences_df = outputDF.sample(4)





    #meal_pref = 'cholesterol'

    #avoid_them = meal_pref
    # print(check_one)
    # check_two = meal_pref+","+check_one
    # print(check_two)

    # diet_pref = check_two.split(",")
    # ret = make_recommendation(outputDF,diet_pref)

    # while (len(ret) == 0):
    #     ret = make_recommendation(outputDF,diet_pref[:-1])
    # print(ret)

    allergies = user_profile['allergies']
    if allergies is not None or allergies !='':
        temp = outputDF[outputDF[allergies]==1].copy()
        allergy_df = temp

    else:
        allergy_df = temp.sample(4)




    #allergies = "soy"
    #avoid_them = allergies
    # check_three = make_allergy(ret,allergies)

    med_con = user_profile['medicalCondition']

    if med_con is not None or med_con !='':
        #med_con = 'diabetes'
        avoid_them =''

        if(med_con == 'diabetes'):
            avoid_them = 'glucose'
        elif(med_con == 'cholesterol'):
            avoid_them = 'cholesterol'
        elif(med_con == 'hypertension'):
            avoid_them = 'sodium'
        elif(med_con == 'pcos'):
            avoid_them = 'glucose,carbohydrate'
        else:
            avoid_them = 'fibre,gluten'



        #print('Here')
        #print(avoid_them)
        avoid_them_preferences = avoid_them.split(',')
        avoid_them_preferences_df = outputDF[outputDF[avoid_them_preferences].sum(axis=1) ==  0].copy()

    else:

        avoid_them_preferences_df = outputDF.sample(4)


    final = pd.concat([diet_preferences_df,avoid_them_preferences_df, meal_pref2_preferences_df, allergy_df])
    #final2 = final.sample(6)


    #optional = optional + med_con
    # final_pref = check_four.split(",")
    # rex = make_final_recomm(ret,final_pref)

    # if len(rex) == 0:
    #     rex = make_final_recomm(final_pref[:-1])
    # print(rex)

    # final= np.array(rex)
    # print(final)
    #final= np.array(ret)

    #final = pd.concat([mandatory_preferences_df.sample(4),avoid_them_preferences_df.sample(2)])


    outputDF.drop_duplicates('meal_id', inplace=True, keep='first')

    #output_list1 = list(outputDF.sample(6)['meal_id'])
    output_list1 = list(final.sample(6)['meal_id'])
    print(output_list1)
    suggest_meals = []
    for i in output_list1:
        suggest_meals.append(outputDF[outputDF['meal_id']==i]['name'].values[0])

    suggest_cal = []
    for i in output_list1:
        suggest_cal.append(int(outputDF[outputDF['meal_id']==i]['calories'].values[0]))
    print(suggest_cal)
    print(outputDF.shape)

    # print(final[0][0])
    # print(final[0][1])
    # print(final[0][2])

    insertInDb(userId, suggest_meals,suggest_cal)

    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Credentials':True
        },
        'body': json.dumps({
            #'user_id':user_id,
            'meal_names':suggest_meals,
            # 'meal_name':final[0][1],
            'calories':suggest_cal
        })
    }

def make_recommendation(outputDF,diet):
    temp = outputDF[outputDF[diet[0]] == 1]
    for i in diet:
        if i == diet[0]:
            continue
        temp = temp[outputDF[i] == 1]
    else:
        return temp
#make_recommendation(['protein','carbohydrate','redmeat','total_fat'])

# diet = 'sodium,carbohydrate,total_fat,cholesterol,protein,fiber,vegan'
# diet_pref = diet.split(",")
# ret = make_recommendation(diet_pref)
# if len(ret) == 0:
#     ret = make_recommendation(diet_pref[:-1])
# print(ret)


def make_allergy(ret,diet):
    temp = ret[ret[diet[0]] == 0]
    for i in diet:
        if i == diet[0]:
            continue
        temp = temp[ret[i] == 0]
    else:
        return temp[["meal_id","name","calories"]]

#make_recommendation(['protein','carbohydrate','redmeat','total_fat'])
# diet = 'seafood,redmeat,pescetarian'
# diet_pref = diet.split(",")
# ret = make_allergy(diet_pref)
# if len(ret) == 0:
#     ret = make_recommendation(diet_pref[:-1])
# print(ret)

def make_final_recomm(temp,diet):
    fix = temp[temp[diet[0]] == 0]
    for i in diet:
        if i == diet[0]:
            continue
        fix = fix[temp[i] == 0]
    else:
        return fix[["meal_id","name","calories"]]

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

def get_user_preferences(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_preferences')
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
    return {}

def insertInDb(user_id, suggest_meals,suggest_cal):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('userRecommendations')
    response = table.get_item(
        Key={
            'userId': user_id
        }
    )
    if 'Item' in response:
        table.update_item(
            Key={
                'userId': user_id
            },
            UpdateExpression='SET recommendationJson = :newRecommendations,recommendedcalories = :calories',
            ExpressionAttributeValues={
                ':newRecommendations': suggest_meals,
                ':calories': suggest_cal
            },

            ReturnValues="UPDATED_NEW"
        )
    else:
        print("Did not found key for this user")
    table.put_item(Item={
        'userId': user_id,
        'recommendationJson':suggest_meals,
        'recommendedcalories':suggest_cal
    })
    # print("DB response when trying to insert data response")
    # print(response)




