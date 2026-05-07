from flask import Blueprint, render_template

# Define the blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('dashboard.html')