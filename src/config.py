import os

DEBUG = False
BCRYPT_LOG_ROUNDS = 12
DATABASE_URI = os.environ.get('DATABASE_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
COLLECTION = os.environ.get('COLLECTION')
