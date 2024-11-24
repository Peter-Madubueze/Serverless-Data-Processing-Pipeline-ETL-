import json

def lambda_handler(event, context):
    # Transform the data (e.g., clean up, modify format)
    raw_data = event['body']
    transformed_data = raw_data.upper()  # Example transformation: convert text to uppercase
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data transformed successfully', 'data': transformed_data})
    }
