import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Only set SSL options for PostgreSQL
    if SQLALCHEMY_DATABASE_URI.startswith('postgresql'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "sslmode": "require"
            }
        }