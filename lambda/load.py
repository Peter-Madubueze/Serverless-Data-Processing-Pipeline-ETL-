import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ETLProcessedData')  # DynamoDB table

def lambda_handler(event, context):
    transformed_data = event['body']
    
    # Simulate loading the transformed data into DynamoDB
    response = table.put_item(
        Item={'id': '1', 'data': transformed_data}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data loaded successfully', 'response': response})
    }
