import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('USERS_TABLE')  # Will use environment variable


def handler(event, context):
    # Logic for selecting random users and initiating a call goes here

    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Call initiated"})  # Modify as needed
    }
    return response
