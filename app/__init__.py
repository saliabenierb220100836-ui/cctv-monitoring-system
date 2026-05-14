import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from sqlalchemy import inspect, text

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))

def ensure_database_schema():
    with db.engine.begin() as connection:
        inspector = inspect(db.engine)
        if 'audit_log' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('audit_log')]
            if 'user_id' not in columns:
                connection.execute(text('ALTER TABLE audit_log ADD COLUMN user_id INTEGER'))
    db.create_all()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'error'

    with app.app_context():
        ensure_database_schema()

    from app.routes.main_routes import main
    app.register_blueprint(main)

    @app.after_request
    def add_no_cache_headers(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return app