from flask import Flask
from dotenv import load_dotenv
import os


load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.config['DEBUG'] = True
app.debug = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

from app import views
from app import admin_views