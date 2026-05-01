from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
# Enable CORS for all routes so the frontend can communicate with this API
CORS(app) 

db_config = {
    'host': os.environ.get('DB_HOST', 'YOUR_DATABASE_EC2_PRIVATE_IP'),
    'user': os.environ.get('DB_USER', 'db_user'),
    'password': os.environ.get('DB_PASSWORD', 'db_password'),
    'database': os.environ.get('DB_NAME', 'app_db')
}

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
            cursor.execute(sql, (data['name'], data['email']))
        connection.commit()
        return jsonify({"message": "User registered successfully in EC2 Database!"}), 201
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/list', methods=['GET'])
def list_users():
    connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, email FROM users")
            users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
