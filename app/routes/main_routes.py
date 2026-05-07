from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from app.models.user import User  
from app import db                

main = Blueprint('main', __name__)

@main.route('/setup-database-xyz')
def setup_database():
    try:
        # --- ADD THIS LINE TEMPORARILY ---
        db.drop_all() 
        
        # Now create the new structure
        db.create_all() 
        
        if not User.query.filter_by(username='felicity').first():
            admin = User(username='felicity')
            admin.set_password('bernabe')
            db.session.add(admin)
            db.session.commit()
            return "<h1>SUCCESS</h1><p>Database wiped and recreated. User 'felicity' created.</p>"
        return "<h1>NOTICE</h1><p>Setup already complete.</p>"
    except Exception as e:
        return f"<h1>ERROR</h1><p>{str(e)}</p>"