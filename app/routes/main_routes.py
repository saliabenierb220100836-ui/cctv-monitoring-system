from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from app.models.user import User  # Corrected to point to your user.py file
from app import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# TEMPORARY ROUTE: Run this once in your browser to create the admin user
@main.route('/setup-admin-99')
def setup_admin():
    db.create_all()  # Verifies or creates the physical database table
    if not User.query.filter_by(username='felicity').first():
        admin = User(username='felicity', password='bernabe')
        db.session.add(admin)
        db.session.commit()
        return "Admin user 'felicity' created successfully! You can now go to /login."
    return "Admin user already exists."