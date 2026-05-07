import os
from flask import render_template, redirect, url_for, request, flash, Blueprint, make_response, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User  
from app.models.log import AuditLog 
from app import db                

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session.permanent = False
            login_user(user, remember=False)
            
            # --- IMPROVED LOGGING ---
            # We record 'Login' as the action and link the user_id for the sidebar/table
            new_log = AuditLog(
                action="Login", 
                ip_address=request.remote_addr,
                user_id=user.id 
            )
            db.session.add(new_log)
            db.session.commit()
            
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')

    response = make_response(render_template('login.html'))
    # Prevent back-button access after logout
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@main.route('/')
@login_required
def index():
    # Only show the latest 5 logs for the dashboard "Recent Activity"
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(5).all()
    camera_url = os.environ.get('CAMERA_URL', 'http://192.168.1.10/snapshot.jpg')
    camera_name = os.environ.get('CAMERA_NAME', 'Main Entrance')
    return render_template('dashboard.html', logs=logs, camera_url=camera_url, camera_name=camera_name)

@main.route('/logs')
@login_required
def logs():
    # Full list for the Activity Logs page
    all_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('logs.html', logs=all_logs)

@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@main.route('/logout')
@login_required # Added this to ensure we have a current_user to log
def logout():
    # --- LOG THE LOGOUT EVENT ---
    new_log = AuditLog(
        action="Logout", 
        ip_address=request.remote_addr,
        user_id=current_user.id
    )
    db.session.add(new_log)
    db.session.commit()
    
    logout_user()
    return redirect(url_for('main.login'))

# Database Setup
@main.route('/setup-database-xyz')
def setup_database():
    try:
        db.drop_all() 
        db.create_all() 
        
        if not User.query.filter_by(username='felicity').first():
            admin = User(username='felicity')
            admin.set_password('bernabe')
            db.session.add(admin)
            db.session.commit()
            return "<h1>SUCCESS</h1><p>Database recreated. User 'felicity' created.</p>"
    except Exception as e:
        return f"<h1>ERROR</h1><p>{str(e)}</p>"