from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))
def create_app():
    # 1. Initialize the Flask object first
    app = Flask(__name__) 
    
    # 2. Load configurations
    app.config.from_object(Config) 

    # 3. Initialize extensions with the app object
    db.init_app(app)
    login_manager.init_app(app)

    # 4. Import and register blueprints inside the function
    from app.routes.main_routes import main
    app.register_blueprint(main)

    return app