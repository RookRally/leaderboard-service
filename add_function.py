import os
import boto3
import json
import random

# Name of environment variable for DynamoDB Table
TABLENAME_ENV_VAR = 'TABLENAME'
START_ELO = 1500


def lambda_handler(event, context):
    # get input parameters
    uid = event['uid']
    name = event['name']

    dist = int(START_ELO * .05)
    elo = START_ELO + random.randint(-dist, dist)

    # get table name for DynamoDB
    #
    if TABLENAME_ENV_VAR in os.environ.keys():
        tablename = os.environ[TABLENAME_ENV_VAR]
    else:
        msg = 'No table name given in ENV via ' + TABLENAME_ENV_VAR
        print(msg)
        return {
            'statusCode': 500,
            'body': json.dumps(msg)
        }

    client = boto3.resource('dynamodb')
    table = client.Table(tablename)

    print('Put item with uid={} to DynamoDB table with name={}'.format(uid, tablename))
    table.put_item(Item={'uid': uid, 'league': 'standard', 'name': name, 'elo': elo})

    return {
        'statusCode': 200,
        'body': json.dumps('addToLeaderboard done.')
    }
