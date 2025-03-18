# src/models/admin_login_model.py

import bcrypt
import httpx

class AdminLoginModel:
    def __init__(self, api_url):
        self.api_url = api_url

    async def authenticate_admin(self, username, password):
        async with httpx.AsyncClient() as client:
            # Authenticate admin using the /admin/login endpoint
            response = await client.post(
                f"{self.api_url}/admin/login",
                json={"username": username, "password": password},
            )
            if response.status_code == 200:
                return True, "Admin login successful!", username
            elif response.status_code == 404:
                return False, "Admin not found!", None
            elif response.status_code == 401:
                return False, "Invalid credentials!", None
            else:
                return False, "Admin login failed!", None