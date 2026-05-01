import json
import boto3
import base64
import os

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'UsersTable')
table = dynamodb.Table(table_name)
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'student-avatars-bucket')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        
        # 1. Decode and Upload Avatar to S3
        if 'avatar_base64' in body and 'avatar_filename' in body:
            image_data = base64.b64decode(body['avatar_base64'])
            s3_client.put_object(Bucket=BUCKET_NAME, Key=body['avatar_filename'], Body=image_data)
        
        # 2. Save to DynamoDB
        table.put_item(
            Item={
                'email': body['email'],
                'name': body['name'],
                'avatar_filename': body.get('avatar_filename')
            }
        )
        
        return {
            'statusCode': 201,
            'headers': {
                'Access-Control-Allow-Origin': '*', # Critical for CORS
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"message": "User registered successfully!"})
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"message": "Internal Server Error"})
        }
