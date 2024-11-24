Here's the updated `setup.md` guide for a **Serverless ETL** pipeline specifically designed for processing data into DynamoDB:

---

# Setup Guide for Serverless ETL with DynamoDB

This document provides a detailed guide for setting up a **Serverless ETL Pipeline** designed to process, transform, and load data into **Amazon DynamoDB**. The solution leverages AWS Lambda, S3, DynamoDB, and supporting AWS services.

---

## Prerequisites

Before you start, ensure you have:
1. **AWS Account** with sufficient permissions.
2. **IAM Permissions**:
   - Full access to DynamoDB, S3, Lambda, and CloudWatch.
   - Permissions to create IAM roles and policies.
3. **Development Environment**:
   - AWS CLI installed and configured.
   - Python 3.x or Node.js installed locally for Lambda development.
   - Terraform or Serverless Framework (optional for deployment automation).
4. **Data Source**: A clear understanding of the data source (e.g., flat files in S3, API, or database).
5. **Data Destination**: A pre-configured DynamoDB table with appropriate schema.

---

## Architecture Overview

### Components
1. **Extract**: Fetches data from the source (e.g., S3 bucket, HTTP API).
2. **Transform**: Processes and transforms data into the desired format.
3. **Load**: Writes the processed data into a DynamoDB table.

### Architecture Diagram
```
[S3] --> [Lambda Extract] --> [Lambda Transform] --> [DynamoDB Load]
```

---

## Setup Steps

### Step 1: Prepare DynamoDB Table
1. **Create a Table**:
   - Use the DynamoDB console or AWS CLI:
     ```bash
     aws dynamodb create-table \
       --table-name YourTableName \
       --attribute-definitions AttributeName=PrimaryKeyName,AttributeType=S \
       --key-schema AttributeName=PrimaryKeyName,KeyType=HASH \
       --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
     ```
   - Replace `PrimaryKeyName` with your primary key attribute.

2. **Define Secondary Indexes** (if needed):
   - Add Global or Local Secondary Indexes for efficient querying.

---

### Step 2: Set Up S3 Bucket
1. Create an S3 bucket for raw data ingestion:
   - Name it (e.g., `etl-source-bucket`).
2. Configure S3 Event Notifications:
   - Enable notifications to trigger the Lambda function for extraction.

3. Example Notification Setup:
   ```bash
   aws s3api put-bucket-notification-configuration --bucket etl-source-bucket --notification-configuration file://notification.json
   ```
   - **notification.json**:
     ```json
     {
       "LambdaFunctionConfigurations": [
         {
           "LambdaFunctionArn": "arn:aws:lambda:region:account-id:function:ExtractFunction",
           "Events": ["s3:ObjectCreated:*"]
         }
       ]
     }
     ```

---

### Step 3: Create IAM Roles and Policies
1. **Lambda Role**:
   - Grant permissions for:
     - Reading from S3.
     - Writing to DynamoDB.
     - Logging to CloudWatch.

2. Example IAM Policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:GetObject",
           "s3:ListBucket",
           "dynamodb:PutItem",
           "dynamodb:BatchWriteItem",
           "logs:CreateLogGroup",
           "logs:CreateLogStream",
           "logs:PutLogEvents"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

---

### Step 4: Configure Lambda Functions
1. **Extract Lambda Function**:
   - Retrieves raw data from S3 or other sources.
   - Example (Python):
     ```python
     import boto3
     def handler(event, context):
         s3 = boto3.client('s3')
         for record in event['Records']:
             bucket = record['s3']['bucket']['name']
             key = record['s3']['object']['key']
             raw_data = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
             return {"status": "success", "data": raw_data.decode("utf-8")}
     ```

2. **Transform Lambda Function**:
   - Processes and structures data.
   - Example:
     ```python
     import json
     def handler(event, context):
         raw_data = event['data']
         transformed_data = json.loads(raw_data)  # Example transformation
         return {"status": "success", "transformed_data": transformed_data}
     ```

3. **Load Lambda Function**:
   - Writes data to DynamoDB.
   - Example:
     ```python
     import boto3
     def handler(event, context):
         dynamodb = boto3.client('dynamodb')
         transformed_data = event['transformed_data']
         for item in transformed_data:
             dynamodb.put_item(
                 TableName='YourTableName',
                 Item={
                     'PrimaryKey': {'S': item['key']},
                     'Data': {'S': item['value']}
                 }
             )
         return {"status": "success"}
     ```

---

### Step 5: Orchestrate with AWS Step Functions
1. **Create a Step Function Workflow**:
   - Define tasks for each Lambda function (Extract, Transform, Load).

2. Example Step Function Definition:
   ```json
   {
     "Comment": "ETL Workflow",
     "StartAt": "Extract",
     "States": {
       "Extract": {
         "Type": "Task",
         "Resource": "arn:aws:lambda:region:account-id:function:ExtractFunction",
         "Next": "Transform"
       },
       "Transform": {
         "Type": "Task",
         "Resource": "arn:aws:lambda:region:account-id:function:TransformFunction",
         "Next": "Load"
       },
       "Load": {
         "Type": "Task",
         "Resource": "arn:aws:lambda:region:account-id:function:LoadFunction",
         "End": true
       }
     }
   }
   ```

---

### Step 6: Automate Deployment (Optional)
1. **Serverless Framework**:
   ```yaml
   service: serverless-etl
   provider:
     name: aws
     runtime: python3.x
   functions:
     extract:
       handler: handler.extract
     transform:
       handler: handler.transform
     load:
       handler: handler.load
   resources:
     Resources:
       DynamoDBTable:
         Type: AWS::DynamoDB::Table
         Properties:
           TableName: YourTableName
           AttributeDefinitions:
             - AttributeName: PrimaryKeyName
               AttributeType: S
           KeySchema:
             - AttributeName: PrimaryKeyName
               KeyType: HASH
   ```

2. **Terraform**: Use Terraform for detailed Infrastructure as Code (IaC) deployment.

---

### Step 7: Monitoring and Error Handling
1. Enable **CloudWatch** logs for Lambda functions.
2. Set up **CloudWatch Alarms** for DynamoDB write errors or throttling.
3. Use **SNS** for email/SMS alerts in case of failures.

---

## Testing the ETL Pipeline
1. **Upload Test Data**: Place sample files in the S3 source bucket.
2. **Validate DynamoDB Entries**: Verify the transformed data in the DynamoDB table.
3. **Review Logs**: Inspect CloudWatch logs for potential issues.

---

## Maintenance
1. Optimize **Lambda Memory**: Adjust memory and timeout settings for cost efficiency.
2. Review **DynamoDB Capacity**:
   - Use Auto Scaling or On-Demand modes as appropriate.
3. Monitor **Cost and Performance**:
   - Use AWS Cost Explorer to track usage.

---

This guide ensures a seamless setup for your **Serverless ETL** pipeline with DynamoDB. Customize the configuration to match your application's specific requirements.

--- 
