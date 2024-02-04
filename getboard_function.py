import json
import os
import boto3

# Name of environment variable for DynamoDB Table
TABLENAME_ENV_VAR = 'TABLENAME'


def lambda_handler(event, context):
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

    client = boto3.client('dynamodb')

    response = client.query(
        TableName=tablename,
        IndexName='league-elo-index',
        ScanIndexForward=False,
        KeyConditionExpression='league = :league',
        ExpressionAttributeValues={
            ':league': {'S': 'standard'}
        }
    )

    opponnents = []
    items = response['Items']
    for item in items:
        player = {
            'uid': item['uid']['S'],
            'name': item['name']['S'],
            'elo': int(item['elo']['N'])
        }
        opponnents.append(player)

    return {
        'statusCode': 200,
        'body': json.dumps(opponnents)
    }
