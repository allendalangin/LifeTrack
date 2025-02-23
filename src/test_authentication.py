import unittest
from unittest.mock import MagicMock
import bcrypt
from New_Authentication import hash_password, check_password, register_user, authenticate_user, users_collection

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        """Set up mock database interactions before each test"""
        self.mock_users = {
            "Allen": hash_password("allenpass")
        }
        users_collection.find_one = MagicMock(side_effect=self.mock_find_one)
        users_collection.insert_one = MagicMock()

    def mock_find_one(self, query):
        """Mock database find_one function"""
        username = query.get("username")
        if username in self.mock_users:
            return {"username": username, "password": self.mock_users[username]}
        return None

    def test_hash_password(self):
        """Test if password hashing works and produces different hashes"""
        password = "testpassword"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)
        self.assertNotEqual(hashed1, hashed2, "Hashing should produce different salts")

    def test_check_password_correct(self):
        """Test if the check_password function works correctly"""
        self.assertTrue(check_password("allenpass", self.mock_users["Allen"]))

    def test_check_password_incorrect(self):
        """Test if an incorrect password fails authentication"""
        self.assertFalse(check_password("wrongpass", self.mock_users["Allen"]))

    def test_register_user_success(self):
        """Test successful user registration"""
        users_collection.find_one.return_value = None  
        success, message = register_user("NewUser", "newpassword")
        self.assertTrue(success)
        self.assertEqual(message, "Signup successful!")
        users_collection.insert_one.assert_called_once()

    def test_register_user_failure(self):
        """Test registering an existing user fails"""
        users_collection.find_one.return_value = {"username": "Allen"}  
        success, message = register_user("Allen", "newpassword")
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists!")

    def test_authenticate_user_success(self):
        """Test successful authentication"""
        success, message = authenticate_user("Allen", "allenpass")
        self.assertTrue(success)
        self.assertEqual(message, "Login successful!")

    def test_authenticate_user_failure(self):
        """Test failed authentication with wrong credentials"""
        success, message = authenticate_user("Allen", "wrongpassword")
        self.assertFalse(success)
        self.assertEqual(message, "Invalid credentials!")

if __name__ == "__main__":
    unittest.main()
