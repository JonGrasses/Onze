from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.models import User  # Import the User model
from bson import ObjectId

mongo = PyMongo()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.login_view = "auth.login"  # Redirect unauthorized users to login page
login_manager.login_message_category = "info"  # Optional: Flash message styling


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mongo.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"

    from app.routes import main
    from app.auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")

    return app

@login_manager.user_loader
def load_user(user_id):
    """Load user from MongoDB using user_id."""
    from app import mongo  # Lazy import to avoid circular import

    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        user_data["_id"] = str(user_data["_id"])  # Ensure _id is a string
        return User(**user_data)
    return None
