import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Fix for Railway/Heroku PostgreSQL strings
    uri = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'

    if SQLALCHEMY_DATABASE_URI.startswith('postgresql'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {"sslmode": "require"}
        }