import json
import requests


def lambda_handler(event, context):
    # TODO implement
    print(event)
    meal_id=event['meal_id'];
    category="";
    if(meal_id=="1"):
        category="lowcarb"
    elif(meal_id=="2"):
        category="glutenfree"
    elif(meal_id=="3"):
        category="nodairy"
    elif(meal_id=="4"):
        category="lowsugar"
    elif(meal_id=="5"):
        category="lowsalt"
    elif(meal_id=="6"):
        category="lowcholestrol"
    elif(meal_id=="7"):
        category="highprotein"
    elif(meal_id=="8"):
        category="highfiber"
    elif(meal_id=="9"):
        category="lowcalorie"
    elif(meal_id=="10"):
        category="lowfat"
    elif(meal_id=="11"):
        category="ovovegan"
    elif(meal_id=="12"):
        category="veganmeal"
    elif(meal_id=="13"):
        category="ovolacvegan"
    elif(meal_id=="14"):
        category="pescetarian"

    headers = {"Content-Type": "application/json"}
    host='https://search-mealview-xxxxxxxxxxxxxxxx.us-east-1.es.amazonaws.com/meals/meal'
    path = host + '/_search?size=24&from=200&q=category:'+category
    print(host)
    print(path)
    response = requests.get(path, headers=headers,auth=('yashika', 'xxxxxxxxxx')).json()
    #print("response from ES", response)
    #dict1 = json.loads(response)
    outoutResp=[];

    for mealsearch in response['hits']['hits']:
        outoutResp.append(mealsearch)

    #print(response['hits']['hits'][0]['_source'])


    return {
        'statusCode': 200,
        'body': json.dumps(outoutResp)
    }
