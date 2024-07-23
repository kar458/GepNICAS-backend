import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database configuration
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST')
FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT')
