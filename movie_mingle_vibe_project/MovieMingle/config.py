import os

class Config:
    IMDB_API_KEY = os.getenv('IMDB_API_KEY', 'your_api_key_here')
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_very_secret_key')