import flet as ft
from New_Login import login_view
from New_Signup import signup_view
from Dashboard import show_dashboard  # Import the dashboard logic
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
        return True, "Login successful!", username  # Return username along with success status and message
    return False, "Invalid credentials!", None

def main(page: ft.Page):
    def route_change(route):
        print(f"Route changed to: {route}")  # Debugging
        page.views.clear()
        if page.route == "/login":
            print("Loading login view...")  # Debugging
            page.views.append(login_view(page, authenticate_user))
        elif page.route == "/signup":
            print("Loading signup view...")  # Debugging
            page.views.append(signup_view(page, register_user))
        elif page.route.startswith("/home"):
            print("Loading dashboard...")  # Debugging
            # Extract username from the route
            username = None
            if "username=" in page.route:
                username = page.route.split("username=")[1]
            page.views.append(show_dashboard(page, username))  # Pass username to the dashboard
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Set the initial route to "/login"
    page.route = "/login"  # Explicitly set the route
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")  # Navigate to the login page

ft.app(target=main)