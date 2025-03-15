# api.py

from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from pydantic import BaseModel
import bcrypt
import base64

# Initialize FastAPI app
app = FastAPI()

# MongoDB Connection
MONGO_URI = "mongodb+srv://shldrlv80:MyMongoDBpass@cluster0.dhh4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
user_db = client["UserData_db"]
stats_db = client["statistics"]
users_collection = user_db["users"]
health_db = client["health_resources"]
infographics_collection = health_db["infographics"]
client_db = client["vaccination"]

# Pydantic model for User
class User(BaseModel):
    username: str
    password: str

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Helper function to verify passwords
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# Endpoint to register a new user
@app.post("/user/")
async def register_user(user: User):
    # Check if the username already exists
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Insert the new user into the database
    users_collection.insert_one({"username": user.username, "password": hashed_password})

    return {"message": "User registered successfully"}

# Endpoint to authenticate a user
@app.get("/user/details/{username}")
async def get_user_details(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user["username"], "password": user["password"]}

# Endpoint to get user details (for debugging or future use)
@app.get("/user/details/{username}")
async def get_user_details(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user["username"], "password": user["password"]}

# Endpoint to get statistics data from MongoDB
@app.get("/stats/{collection_name}")
async def get_statistics(collection_name: str):
    if collection_name == "by_year":
        data = list(stats_db.by_year.find({}, {"_id": 0}))
    elif collection_name == "by_region":
        data = list(stats_db.by_region.find({}, {"_id": 0}))
    else:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    return data

@app.get("/vaccination_schedules")
async def get_vaccination_schedules():
    """Fetch all vaccination schedules from MongoDB."""
    schedules = list(client_db["vaccination_schedules"].find({}, {"_id": 0}))  # Exclude _id field
    if schedules:
        print(schedules)
        return schedules
    raise HTTPException(status_code=404, detail="No vaccination schedules found.")

@app.put("/user/update_username")
async def update_username(old_username: str, new_username: str):
    user = users_collection.find_one({"username": old_username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if users_collection.find_one({"username": new_username}):
        raise HTTPException(status_code=400, detail="Username already taken")

    users_collection.update_one({"username": old_username}, {"$set": {"username": new_username}})
    return {"message": "Username updated successfully"}


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)