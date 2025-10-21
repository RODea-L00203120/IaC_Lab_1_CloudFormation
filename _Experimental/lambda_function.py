import json

def handler(event, context):
    # This code is designed to be triggered by API Gateway
    # It gets the source IP from the 'requestContext'
    ip_address = event['requestContext']['identity']['sourceIp']

    return {
        'body': json.dumps({"ip_address": ip_address}),
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200
    }