import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Email Configuration
    EMAIL_SERVER = os.getenv('EMAIL_SERVER', 'imap.gmail.com')
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Database Configuration
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///emails.db')
    
    # App Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')