"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages orders for flowers.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'OrderFlowers' template.
For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""
import math
import dateutil.parser
import datetime
import time
import os
import logging
import boto3
import json
import re
import pandas as pd
import numpy as np

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """
def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def food_info(foodname):

    # foodnames = ['nuts','fish','lamb','chicken','broccoli','cornstarch']
    if type(foodname) != str:
        return build_validation_result(False,
                                       'foodname',
                                       'Please enter a string')

    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """

def validate_dining_suggestion(location, cuisine, time, date, numberOfPeople):

    regex = '^[a-z 0-9]+[\._}?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
    locations = ['manhattan', 'brooklyn', 'bronx','queens','staten island']
    if location is not None and location.lower() not in locations:
        return build_validation_result(False,
                                       'Location',
                                       'We do not have suggestions for {}, would you like suggestions for a different location?  '
                                       'Our most popular location is Manhattan '.format(location))

    cuisines = ['chinese', 'indian', 'italian', 'mexican', 'thai','japanese']
    if cuisine is not None and cuisine.lower() not in cuisines:
        return build_validation_result(False,
                                       'Cuisine',
                                       'We do not have suggestions for {}, would you like suggestions for a different cuisine ?  '
                                       'Our most popular Cuisine is Indian '.format(cuisine))
    if date is not None:
        if not isvalid_date(date):
            return build_validation_result(False, 'Date', 'I did not understand that, what date would you like to have the recommendation for?')
        elif datetime.datetime.strptime(date, '%Y-%m-%d').date() < datetime.date.today():
            return build_validation_result(False, 'Date',  'Sorry, that is not possible.What day would you like to have the recommendation for?')


    if time is not None:
        if len(time) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'DiningTime', None)

        hour, minute = time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)

        HOUR        = datetime.datetime.now().hour
        MINUTE      = datetime.datetime.now().minute
        SECONDS     = datetime.datetime.now().second

        print(HOUR, MINUTE, SECONDS)

        if datetime.datetime.strptime(date, '%Y-%m-%d').date() == datetime.date.today():
            if hour <= HOUR and minute <= MINUTE:
                return build_validation_result(False, 'Time', 'You are trying to book for a past-time. Please check, Our business hours are from 10 AM. to 11 PM. Can you specify a time during this range?')

        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'Time', None)

        if hour < 10 or hour > 24:
            # Outside of business hours
            return build_validation_result(False, 'Time', 'Our business hours are from 10 AM. to 11 PM. Can you specify a time during this range?')

    if numberOfPeople is not None:
        numberOfPeople = int(numberOfPeople)
        if numberOfPeople > 20 or numberOfPeople <= 0:
            return build_validation_result(False,
                                           'NumberOfPeople',
                                           'That does not look like a valid number {}, '
                                           'It should be less than 20'.format(numberOfPeople))

    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def diningSuggestions(intent_request,context):

    location = get_slots(intent_request)["Location"]
    cuisine = get_slots(intent_request)["Cuisine"]
    date = get_slots(intent_request)["Date"]
    time = get_slots(intent_request)["Time"]
    numberOfPeople = get_slots(intent_request)["NumberOfPeople"]
    #phoneNumber = get_slots(intent_request)["PhoneNumber"]
    #email = get_slots(intent_request)["Email"]
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    requestData = {
        "cuisine": cuisine,
        "location":location,
        "categories":cuisine,
        "limit":"3",
        "peoplenum": numberOfPeople,
        "Date": date,
        "Time": time
        #"Email": email,
        #"PhoneNum": phoneNumber
    }

    print (requestData)
    # output_session_attributes = {}
    output_session_attributes['requestData'] = json.dumps(requestData)

    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validation_result = validate_dining_suggestion(location, cuisine, time, date, numberOfPeople)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])
        # output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return delegate(output_session_attributes, get_slots(intent_request))

    #record(intent_request)
    messageId = sendSQSMessage(requestData)
    print (messageId)
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Thank you for the information, we are generating our recommendations!'})

def findinfo(intent_request,context):

    foodname = get_slots(intent_request)["foodname"]
    source = intent_request['invocationSource']
    s3 = boto3.client('s3')
    nutritionaldata = s3.get_object(Bucket='mealdeliveryapp', Key='Resources/Kmeansoutput/nutritionfacts.csv')
    nutritionDF = pd.read_csv(nutritionaldata['Body'])

    search_this = str(foodname)

    search_df = nutritionDF[nutritionDF['name'].apply(lambda x: True if (search_this.lower() in x.lower()) else False)].copy()
    search_df_result = search_df[['name','calories','total_fat','cholesterol','fiber','sugars']].sample(1)
    # result = str(search_df_result.to_json())

    meal_name = str(search_df_result['name'].iloc[0])
    calories = str(search_df_result['calories'].iloc[0])
    total_fat = str(search_df_result['total_fat'].iloc[0])
    cholesterol = str(search_df_result['cholesterol'].iloc[0])
    fiber = str(search_df_result['fiber'].iloc[0])
    sugars = str(search_df_result['sugars'].iloc[0])

    # result = "Meal Name:" + meal_name + '\n'
    # +"Calorie count:" +calories+  '\n'
    # +"Total Fat:"+ total_fat +'\n'
    # + "Total Cholesterol:"+ cholesterol
    # + '\n' +"Total Fiber:" +fiber + '\n'
    # + "Total Sugar:"+sugars

    # print(result)

    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    requestData = {"foodname": foodname}

    print (requestData)
    # output_session_attributes = {}
    output_session_attributes['requestData'] = json.dumps(requestData)

    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validation_result = food_info(foodname)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])
        # output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return delegate(output_session_attributes, get_slots(intent_request))
    # messageId = sendSQSMessage(requestData)
    # print (messageId)
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Thank you heres the nutrional info :'
                             +'\n' + "Meal Name:" + meal_name
                             + '\n' +"Calorie count:" +calories
                             + '\n' +"Total Fat:"+ total_fat
                             + '\n' + "Total Cholesterol:"+ cholesterol
                             + '\n' +"Total Fiber:" +fiber
                             + '\n' + "Total Sugar:"+sugars})

def sendSQSMessage(requestData):
    queue_url = 'https://sqs.us-east-1.amazonaws.com/189825224419/chatbotqueue'
    sqs = boto3.client('sqs', region_name='us-east-1')


    messageAttributes = {
        'Cuisine': {
            'DataType': 'String',
            'StringValue': requestData['cuisine']
        },
        'Location': {
            'DataType': 'String',
            'StringValue': requestData['location']
        },
        'Categories': {
            'DataType': 'String',
            'StringValue': requestData['categories']
        },
        "DiningTime": {
            'DataType': "String",
            'StringValue': requestData['Time']
        },
        "DiningDate": {
            'DataType': "String",
            'StringValue': requestData['Date']
        },
        'PeopleNum': {
            'DataType': 'Number',
            'StringValue': requestData['peoplenum']
        }
        # 'Email': {
        #     'DataType': 'String',
        #     'StringValue': requestData['Email']
        # },
        # 'PhoneNum': {
        #     'DataType': 'Number',
        #     'StringValue': requestData['PhoneNum']
        # }
    }
    #mesAtrributes = json.dumps(messageAttributes)
    messageBody=('Slots for the Restaurant')
    #print mesAtrributes
    print(messageBody)

    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes = messageAttributes,
        MessageBody = messageBody)

    print(response)
    print("Message sent on queue")

    return response['MessageId']

""" --- Intents --- """

def welcome(intent_request):
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Hey there, How may I serve you today?'})

def thankYou(intent_request):
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'My pleasure, Have a great day!!'})


def dispatch(intent_request,context):
    """
    Called when the user specifies an intent for this bot.
    """

    #logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'DiningSuggestionsIntent':
        return diningSuggestions(intent_request,context)
    elif intent_name == 'ThankYouIntent':
        return thankYou(intent_request)
    elif intent_name == 'GreetingIntent':
        return welcome(intent_request)
    elif intent_name == 'FindNutritionalInfo':
        return findinfo(intent_request,context)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    #logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event,context)
    
