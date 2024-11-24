import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Extract S3 event details
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Download the file from S3
    file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    file_content = file_obj['Body'].read().decode('utf-8')
    
    # For demonstration, we're simply returning the content of the file
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'File extracted successfully', 'content': file_content})
    }
