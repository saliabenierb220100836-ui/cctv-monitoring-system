import os
import urllib.request
import urllib.error
from flask import render_template, redirect, url_for, request, flash, Blueprint, make_response, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.models.log import AuditLog
from app import db

main = Blueprint('main', __name__)


def get_device():
    ua = request.user_agent.string.lower()
    if 'iphone' in ua:
        return 'iPhone'
    elif 'ipad' in ua:
        return 'iPad'
    elif 'android' in ua and 'mobile' in ua:
        return 'Android Phone'
    elif 'android' in ua:
        return 'Android Tablet'
    elif 'windows' in ua:
        return 'Windows'
    elif 'macintosh' in ua or 'mac os' in ua:
        return 'Mac'
    elif 'linux' in ua:
        return 'Linux'
    else:
        return 'Unknown Device'


def check_camera_live(camera_url, timeout=3):
    if not camera_url:
        return False
    try:
        req = urllib.request.Request(camera_url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False


def log_action(action):
    entry = AuditLog(
        action=action,
        ip_address=request.remote_addr,
        device=get_device(),
        user_id=current_user.id
    )
    db.session.add(entry)
    db.session.commit()


# ─── Public Routes ────────────────────────────────────────────────────────────

@main.route('/')
def home():
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session.permanent = False
            login_user(user, remember=False)
            entry = AuditLog(
                action="Login",
                ip_address=request.remote_addr,
                device=get_device(),
                user_id=user.id
            )
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


# ─── Protected Routes ─────────────────────────────────────────────────────────

@main.route('/dashboard')
@login_required
def dashboard():
    camera_url = os.environ.get('CAMERA_URL', '')
    camera_name = os.environ.get('CAMERA_NAME', 'Main Entrance')
    camera_online = check_camera_live(camera_url)
    return render_template('dashboard.html',
                           camera_url=camera_url,
                           camera_name=camera_name,
                           camera_online=camera_online)


@main.route('/logs')
@login_required
def logs():
    all_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('logs.html', logs=all_logs)


@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@main.route('/update-username', methods=['POST'])
@login_required
def update_username():
    new_username = request.form.get('username', '').strip()

    if not new_username:
        flash('Username cannot be empty.', 'error')
        return redirect(url_for('main.settings'))

    taken = User.query.filter_by(username=new_username).first()
    if taken and taken.id != current_user.id:
        flash('Username is already taken.', 'error')
        return redirect(url_for('main.settings'))

    current_user.username = new_username
    db.session.commit()
    log_action("Changed Username")
    flash('Username updated successfully.', 'success')
    return redirect(url_for('main.settings'))


@main.route('/update-password', methods=['POST'])
@login_required
def update_password():
    current_pw = request.form.get('current_password', '')
    new_pw = request.form.get('new_password', '')
    confirm_pw = request.form.get('confirm_password', '')

    if not current_user.check_password(current_pw):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('main.settings'))

    if new_pw != confirm_pw:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('main.settings'))

    if len(new_pw) < 6:
        flash('Password must be at least 6 characters.', 'error')
        return redirect(url_for('main.settings'))

    current_user.set_password(new_pw)
    db.session.commit()
    log_action("Changed Password")
    flash('Password updated successfully.', 'success')
    return redirect(url_for('main.settings'))


@main.route('/logout')
@login_required
def logout():
    log_action("Logout")
    logout_user()
    return redirect(url_for('main.login'))


# ─── Setup (run once) ─────────────────────────────────────────────────────────

@main.route('/setup-database-xyz')
def setup_database():
    try:
        db.drop_all()
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        return "<h1>SUCCESS</h1><p>Database ready. Login: admin / admin123</p>"
    except Exception as e:
        return f"<h1>ERROR</h1><p>{str(e)}</p>"