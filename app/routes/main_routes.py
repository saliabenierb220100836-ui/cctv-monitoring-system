from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from app.models.user import User  # Corrected path to the models folder
from app import db                # Needed for the setup route

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # These match the 'name' attribute in your HTML input fields
        username = request.form.get('username') 
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        # Simple password check
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html')

@main.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --- SECRET SETUP ROUTE ---
# Visit: https://your-railway-link.app/setup-database-xyz
@main.route('/setup-database-xyz')
def setup_database():
    try:
        db.create_all()  # Creates the 'user' table in your database
        if not User.query.filter_by(username='felicity').first():
            admin = User(username='felicity', password='bernabe')
            db.session.add(admin)
            db.session.commit()
            return "SUCCESS: Table created and user 'felicity' added!"
        return "NOTICE: User already exists."
    except Exception as e:
        return f"ERROR: {str(e)}"