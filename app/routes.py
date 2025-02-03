from flask import Blueprint, render_template
from flask_login import login_required

# Define the Blueprint
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    return "<h1>Welcome to the Onze Gym Dashboard</h1>"
