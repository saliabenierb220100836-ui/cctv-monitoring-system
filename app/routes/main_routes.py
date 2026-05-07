from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from app.models.user import User  
from app import db                

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.index'))
        
        flash('Login Unsuccessful. Please check credentials.', 'danger')
    return render_template('login.html')

@main.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --- SECRET SETUP URL ---
# Visit this URL once: https://your-app-name.railway.app/setup-database-xyz
@main.route('/setup-database-xyz')
def setup_database():
    try:
        db.create_all() 
        if not User.query.filter_by(username='felicity').first():
            admin = User(username='felicity', password='bernabe')
            db.session.add(admin)
            db.session.commit()
            return "<h1>SUCCESS</h1><p>User 'felicity' created. <a href='/login'>Login here</a></p>"
        return "<h1>NOTICE</h1><p>User already exists.</p>"
    except Exception as e:
        return f"<h1>ERROR</h1><p>{str(e)}</p>"