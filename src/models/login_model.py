# src/models/login_model.py

import bcrypt
import httpx

class UserModel:
    def __init__(self, api_url):
        self.api_url = api_url

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    async def register_user(self, username, password):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/user/",
                json={"username": username, "password": password},  # Send plain password
            )
            if response.status_code == 200:
                return True, "Signup successful!"
            elif response.status_code == 400:
                return False, "Username already exists!"
            else:
                return False, "Signup failed!"

    async def authenticate_user(self, username, password):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/user/details/{username}")
            if response.status_code == 200:
                user_data = response.json()
                if self.check_password(password, user_data["password"]):
                    return True, "Login successful!", username
            return False, "Invalid credentials!", None