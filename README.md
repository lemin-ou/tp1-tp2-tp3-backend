# TP3: Serverless Deployment Guide

In this TP, we will abandon our EC2 and RDS instances and move to a fully Serverless architecture.

## Part 1: Console Deployment (For this TP)

**1. Create the DynamoDB Table**
* Go to DynamoDB -> Create Table.
* Name: `UsersTable`
* Partition Key: `email` (String)

**2. Create the IAM Role**
* Go to IAM -> Roles -> Create Role (Trusted entity: Lambda).
* Attach policies: `AmazonS3FullAccess` and `AmazonDynamoDBFullAccess`. (Note: In a real environment, you would restrict this to only the specific bucket and table).

**3. Create the Lambda Functions**
* Create Function 1: `RegisterUser` (Python 3.9+). Attach the IAM role. Paste the code from `register_lambda.py`.
* Create Function 2: `ListUsers` (Python 3.9+). Attach the IAM role. Paste the code from `list_lambda.py`.
* *Environment Variables*: For both Lambdas, go to Configuration -> Environment variables. Add `S3_BUCKET_NAME` (e.g., `student-avatars-bucket`) and `DYNAMODB_TABLE` (`UsersTable`).
* *Important:* Ensure you click **Deploy** in the code source editor.

**4. Configure API Gateway & CORS**
* Go to API Gateway -> Create REST API.
* Create Resource: `/register`. Create Method: `POST`. Link to `RegisterUser` Lambda.
* Create Resource: `/list`. Create Method: `GET`. Link to `ListUsers` Lambda.
* **CRITICAL FOR FRONTEND:** Click on `/register`, click **Enable CORS**. Do the same for `/list`. This allows your browser frontend to talk to the API.
* Click **Deploy API** to a new stage (e.g., `dev`). Copy the Invoke URL.

---

## Part 2: Future Reference - Infrastructure as Code (AWS SAM)

While we used the AWS Console for this TP to understand the moving parts, professionals automate this process. Below is an **AWS Serverless Application Model (SAM)** template. 

If you install the AWS SAM CLI, you can deploy this entire infrastructure (API Gateway, both Lambdas, DynamoDB, and IAM roles) by simply running `sam deploy --guided` in your terminal.

**`template.yaml` (Reference Only)**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Serverless User API

Globals:
  Function:
    Timeout: 3
    Environment:
      Variables:
        S3_BUCKET_NAME: student-avatars-bucket
        DYNAMODB_TABLE: UsersTable
  Api:
    Cors:
      AllowMethods: "'GET,POST,OPTIONS'"
      AllowHeaders: "'Content-Type'"
      AllowOrigin: "'*'" # Automates the CORS configuration we did in the console

Resources:
  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: UsersTable
      AttributeDefinitions:
        - AttributeName: email
          AttributeType: S
      KeySchema:
        - AttributeName: email
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST

  RegisterFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: register_lambda.lambda_handler
      Runtime: python3.9
      Policies:
        - S3CrudPolicy:
            BucketName: student-avatars-bucket
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
      Events:
        RegisterApi:
          Type: Api
          Properties:
            Path: /register
            Method: post

  ListFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: list_lambda.lambda_handler
      Runtime: python3.9
      Policies:
        - S3ReadPolicy:
            BucketName: student-avatars-bucket
        - DynamoDBReadPolicy:
            TableName: !Ref UsersTable
      Events:
        ListApi:
          Type: Api
          Properties:
            Path: /list
            Method: get
```
