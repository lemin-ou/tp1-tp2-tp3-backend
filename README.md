# AWS TP Backend - IaaS Baseline (TP1)

This repository contains the backend Flask application for TP1. It connects to a manually provisioned MySQL database on another EC2 instance.

## Setup Instructions

1.  SSH into your API EC2 instance.
2.  Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
3.  Set up your environment variables by copying `.env.sample` to `.env`:
    ```bash
    cp .env.sample .env
    ```
4.  Edit the `.env` file to point to your Database EC2 instance's private IP.
    ```bash
    DB_HOST="YOUR_DATABASE_EC2_PRIVATE_IP"
    DB_USER="db_user"
    DB_PASSWORD="db_password"
    DB_NAME="app_db"
    ```
5.  Run the application on port 80 (requires sudo):
    ```bash
    sudo python3 app.py
    ```
