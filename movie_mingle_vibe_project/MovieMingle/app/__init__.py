from flask import Flask
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# Instantiate Redis client
redis_client = Redis(host='localhost', port=6379, db=0)

from app import routes, errors, models, utils