import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Get the raw URL from Railway
    uri = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    
    # Fix the protocol for SQLAlchemy compatibility
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'

    # Enable SSL for production PostgreSQL
    if SQLALCHEMY_DATABASE_URI.startswith('postgresql'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "sslmode": "require"
            }
        }