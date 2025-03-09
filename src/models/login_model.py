# src/models/login_model.py

import bcrypt

class UserModel:
    def __init__(self, users_collection):
        self.users_collection = users_collection

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def register_user(self, username, password):
        if self.users_collection.find_one({"username": username}):
            return False, "Username already exists!"
        hashed_pw = self.hash_password(password)
        self.users_collection.insert_one({"username": username, "password": hashed_pw})
        return True, "Signup successful!"

    def authenticate_user(self, username, password):
        user = self.users_collection.find_one({"username": username})
        if user and self.check_password(password, user["password"]):
            return True, "Login successful!", username
        return False, "Invalid credentials!", None