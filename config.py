import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 1. Prioritize the Railway Environment Variable
    uri = os.environ.get('DATABASE_URL')
    
    # 2. If URI is missing (local dev), fallback to SQLite
    if not uri:
        uri = 'sqlite:///site.db'
    
    # 3. Fix the 'postgres://' vs 'postgresql://' issue for SQLAlchemy 1.4+
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-123')

    # 4. Mandatory SSL for Railway PostgreSQL
    if "postgresql" in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "sslmode": "require"
            }
        }