from flask_login import UserMixin
from bson import ObjectId

class User(UserMixin):
    def __init__(self, username, email, password=None, password_hash=None, role="client", _id=None):
        self.id = str(_id) if _id else None  # Convert _id to string
        self.username = username
        self.email = email
        self.role = role

        if password:
            self.set_password(password)  # Hash and store password
        else:
            self.password_hash = password_hash  # Use existing hash

    def set_password(self, password):
        """Hash the password before saving"""
        from app import bcrypt  # Lazy import to avoid circular import
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        from app import bcrypt  # Lazy import
        return bcrypt.check_password_hash(self.password_hash, password)

    def save(self):
        """Save user to MongoDB"""
        from app import mongo  # Lazy import

        user_data = {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role
        }
        if self.id:
            user_data["_id"] = ObjectId(self.id)

        result = mongo.db.users.insert_one(user_data)
        self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_email(email):
        """Find a user by email"""
        from app import mongo  # Lazy import

        user_data = mongo.db.users.find_one({"email": email})
        if user_data:
            # Convert ObjectId to string
            user_data["_id"] = str(user_data["_id"])
            return User(**user_data)  # Now it correctly handles password_hash
        return None
