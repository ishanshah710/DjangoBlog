import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DJANGO_SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PWD = os.environ.get('DB_PWD')
DB_NAME = os.environ.get('DB_NAME')