import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://postgres:rysPxkSTIrXgEwDAsBJaCdieHjMUUwfm@turntable.proxy.rlwy.net:12704/railway_DB}}') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "sslmode": "require"
        }
    }