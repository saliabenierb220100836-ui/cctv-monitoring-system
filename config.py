import os

class Config:
    # 1. Pull the URL from Railway's environment
    uri = os.environ.get('DATABASE_URL')
    
    # 2. Critical: Fix the 'postgres://' vs 'postgresql://' prefix
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    # 3. Fallback only for local testing
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///site.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 4. Mandatory SSL for Railway cloud database
    if uri and "postgresql" in uri:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {"sslmode": "require"}
        }