import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Safely retrieve the Railway DATABASE_URL
    raw_uri = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    
    # Fix protocol prefix for SQLAlchemy compatibility
    if raw_uri.startswith("postgres://"):
        raw_uri = raw_uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = raw_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-dev-key'

    # Ensure SSL is used for the remote PostgreSQL connection
    if SQLALCHEMY_DATABASE_URI.startswith('postgresql'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {"sslmode": "require"}
        }