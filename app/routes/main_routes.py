from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User  
from app.models.log import AuditLog # Import your log model
from app import db                

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        # Use the new check_password method
        if user and user.check_password(password):
            login_user(user)
            
            # --- ADD REAL LOG HERE ---
            new_log = AuditLog(action=f"User {username} logged in", ip_address=request.remote_addr)
            db.session.add(new_log)
            db.session.commit()
            
            return redirect(url_for('main.index'))
        
        flash('Login Unsuccessful.', 'danger')
    return render_template('login.html')

@main.route('/')
@login_required
def index():
    # Fetch real logs from DB to show on dashboard
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', logs=logs)

# Update your setup route to use hashing
@main.route('/setup-database-xyz')
def setup_database():
    db.create_all() 
    if not User.query.filter_by(username='felicity').first():
        admin = User(username='felicity')
        admin.set_password('bernabe') # This hashes it!
        db.session.add(admin)
        db.session.commit()
        return "Database Setup Complete."
    return "Already setup."