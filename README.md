# AWS TP Backend - IaaS Baseline (TP1)

This repository contains the backend Flask application for TP1. It connects to a manually provisioned MySQL database on another EC2 instance.

## Setup Instructions

1.  SSH into your API EC2 instance.
2.  Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
3.  Set your environment variables (or edit `app.py` directly) to point to your Database EC2 instance's private IP.
    ```bash
    export DB_HOST="YOUR_DATABASE_EC2_PRIVATE_IP"
    export DB_USER="db_user"
    export DB_PASSWORD="db_password"
    export DB_NAME="app_db"
    ```
4.  Run the application on port 80 (requires sudo):
    ```bash
    sudo python3 app.py
    ```
