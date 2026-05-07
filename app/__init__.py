from datetime import datetime, timedelta

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None
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


def format_ph_time(value, fmt='%Y-%m-%d %H:%M:%S'):
    if value is None:
        return ''
    if not isinstance(value, datetime):
        return value
    if value.tzinfo is None:
        return value.strftime(fmt)
    if ZoneInfo:
        try:
            return value.astimezone(ZoneInfo('Asia/Manila')).strftime(fmt)
        except Exception:
            pass
    return (value + timedelta(hours=8)).strftime(fmt)


def create_app():
    app = Flask(__name__)  # No spaces before 'app'
    app.config.from_object(Config)

    app.jinja_env.cache = {}
    app.jinja_env.filters['ph_time'] = format_ph_time

    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'main.login'

    # Blueprint registration
    from app.routes.main_routes import main
    app.register_blueprint(main)

    return app