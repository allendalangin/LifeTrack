import flet as ft
from New_Login import login_view
from New_Signup import signup_view
from home_view import home_view
import pymongo
import bcrypt

# MongoDB Connection (Replace with your MongoDB URI)
MONGO_URI = "mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_URI)
db = client["UserData_db"]  # Database name
users_collection = db["users"]  # Collection name

# Helper functions for authentication
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return False, "Username already exists!"
    hashed_pw = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_pw})
    return True, "Signup successful!"

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and check_password(password, user["password"]):
        return True, "Login successful!"
    return False, "Invalid credentials!"

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(login_view(page, authenticate_user))
        elif page.route == "/signup":
            page.views.append(signup_view(page, register_user))
        elif page.route == "/home":
            page.views.append(home_view(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

ft.app(target=main)
