from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.models import User  # Import the User model

mongo = PyMongo()
login_manager = LoginManager()
bcrypt = Bcrypt()

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
    """Load user from MongoDB using the user_id."""
    user_data = mongo.db.users.find_one({"_id": user_id})
    if user_data:
        return User(**user_data, _id=user_data["_id"])
    return None
