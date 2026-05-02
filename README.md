# AWS TP Backend - PaaS & Secure Storage (TP2)

This repository contains the backend Flask application for TP2. It connects to a managed Amazon RDS database and uses an IAM Instance Profile to securely interact with Amazon S3.

## Setup Instructions

1.  Attach an IAM Role to your EC2 instance with `AmazonS3FullAccess` (or a custom scoped policy).
2.  SSH into your API EC2 instance.
3.  Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
4.  Set up your environment variables by copying `.env.sample` to `.env`:
    ```bash
    cp .env.sample .env
    ```
5.  Edit the `.env` file to point to your RDS Endpoint and S3 bucket:
    ```bash
    S3_BUCKET_NAME="student-avatars-bucket"
    DB_HOST="YOUR_RDS_ENDPOINT.amazonaws.com"
    DB_USER="db_user"
    DB_PASSWORD="db_password"
    DB_NAME="app_db"
    ```
6.  Run the application on port 80 (requires sudo):
    ```bash
    sudo python3 app.py
    ```
