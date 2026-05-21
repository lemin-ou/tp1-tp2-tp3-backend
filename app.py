from botocore.config import Config
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql
import boto3
import base64
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes so the frontend can communicate with this API
CORS(app) 

# Uses IAM Instance Profile credentials automatically (no access keys needed)
s3_client = boto3.client('s3', config=Config(signature_version='s3v4', region_name=os.environ.get('AWS_REGION'))) 
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'student-avatars-bucket')

db_config = {
    'host': os.environ.get('DB_HOST', 'YOUR_RDS_ENDPOINT.amazonaws.com'),
    'user': os.environ.get('DB_USER', 'db_user'),
    'password': os.environ.get('DB_PASSWORD', 'db_password'),
    'database': os.environ.get('DB_NAME', 'app_db')
}

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    
    try:
        # 1. Decode Base64 and Upload Avatar to S3
        image_data = base64.b64decode(data['avatar_base64'])
        s3_client.put_object(Bucket=BUCKET_NAME, Key=data['avatar_filename'], Body=image_data)
    except Exception as e:
        print(f"S3 Upload error: {e}")
        return jsonify({"message": "Failed to upload avatar to S3"}), 500

    try:
        # 2. Save to RDS Database (We only store the filename)
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (name, email, avatar_filename) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data['name'], data['email'], data['avatar_filename']))
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"message": "Database Error"}), 500
    
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/list', methods=['GET'])
def list_users():
    try:
        connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, email, avatar_filename FROM users")
            users = cursor.fetchall()
        connection.close()
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"message": "Database Error"}), 500

    # Generate Presigned GET URLs for each user
    try:
        for user in users:
            if user.get('avatar_filename'):
                presigned_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': user['avatar_filename']},
                    ExpiresIn=3600 # URL valid for 1 hour
                )
                user['userAvatarUrl'] = presigned_url
            else:
                user['userAvatarUrl'] = None
    except Exception as e:
        print(f"S3 Presigned URL error: {e}")
        # Even if URL generation fails, we can still return the users
    
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
