from flask import Blueprint, render_template

# Define the Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    return "<h1>Welcome to the Onze Gym Dashboard</h1>"
