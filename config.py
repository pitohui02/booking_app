from dotenv import load_dotenv
import os

# Load environment variables from .env file

load_dotenv()

# DATABASE

class Config:
    
    DB_URL = os.getenv('DB_URL')
    