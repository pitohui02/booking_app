import sys
import os

from dotenv import load_dotenv


# Add the parent directory to the system path to allow imports from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file

load_dotenv()

# Credentials 
class Config:
    
    DB_URL = os.getenv("DB_URL", f"sqlite:///{os.path.join(BASE_DIR, 'booking.db')}")