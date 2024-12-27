from flask import Flask
from dotenv import load_dotenv
import os


load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.config['DEBUG'] = True
app.debug = True

from app import views
from app import admin_views