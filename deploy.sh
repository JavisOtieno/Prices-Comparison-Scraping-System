#!/bin/bash

# Navigate to the application directory
cd /var/www/myflaskapp

# Pull the latest code from the main branch
#git pull origin main

# Activate the virtual environment
source venv/bin/activate

# Install the required dependencies
#pip install -r requirements.txt

# Touch the WSGI file to trigger a reload
touch /var/www/myflaskapp/myflaskapp.wsgi

