from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
PORT = os.getenv('PORT')
WS_EINVOICES_URL = os.getenv('WS_EINVOICES_URL')
WS_DATABASE_NAME = os.getenv('WS_DATABASE_NAME')