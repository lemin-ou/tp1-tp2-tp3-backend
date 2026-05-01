# AWS TP Backend - PaaS & Secure Storage (TP2)

This repository contains the backend Flask application for TP2. It connects to a managed Amazon RDS database and uses an IAM Instance Profile to securely interact with Amazon S3.

## Setup Instructions

1.  Attach an IAM Role to your EC2 instance with `AmazonS3FullAccess` (or a custom scoped policy).
2.  SSH into your API EC2 instance.
3.  Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
4.  Set your environment variables to point to your RDS Endpoint and S3 bucket:
    ```bash
    export S3_BUCKET_NAME="student-avatars-bucket"
    export DB_HOST="YOUR_RDS_ENDPOINT.amazonaws.com"
    export DB_USER="db_user"
    export DB_PASSWORD="db_password"
    export DB_NAME="app_db"
    ```
5.  Run the application on port 80 (requires sudo):
    ```bash
    sudo python3 app.py
    ```
