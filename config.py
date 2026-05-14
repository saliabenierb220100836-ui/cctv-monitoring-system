import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://postgres:rysPxkSTIrXgEwDAsBJaCdieHjMUUwfm@postgres.railway.internal:5432/') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    WTF_CSRF_ENABLED = False
    TEMPLATES_AUTO_RELOAD = True