import json
import boto3
import os

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'UsersTable')
table = dynamodb.Table(table_name)
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'student-avatars-bucket')

def lambda_handler(event, context):
    try:
        # Scan DynamoDB (Note: Scan is fine for a TP, but Query is better for production)
        response = table.scan()
        users = response.get('Items', [])
        
        # Generate Presigned URLs
        for user in users:
            if user.get('avatar_filename'):
                try:
                    presigned_url = s3_client.generate_presigned_url(
                        'get_object',
                        Params={'Bucket': BUCKET_NAME, 'Key': user['avatar_filename']},
                        ExpiresIn=3600
                    )
                    user['userAvatarUrl'] = presigned_url
                except Exception as e:
                    print(f"Error generating presigned URL for {user.get('email')}: {e}")
                    user['userAvatarUrl'] = None
                
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*', # Critical for CORS
                'Content-Type': 'application/json'
            },
            'body': json.dumps(users)
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
