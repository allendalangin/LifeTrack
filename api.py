# api.py

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from pymongo import MongoClient
from pydantic import BaseModel
import bcrypt
import cloudinary
import cloudinary.uploader
import cloudinary.api
from bson import ObjectId

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
vaccination_schedules_collection = client_db["vaccination_schedules"]
health_hotlines_collection = health_db["health_hotlines"]
admin_collection = user_db["admin"]  # Add the admin collection

# Cloudinary Configuration
cloudinary.config(
    cloud_name="your_cloud_name",  # Replace with your Cloudinary cloud name
    api_key="348841966416776",     # Your Cloudinary API key
    api_secret="G5OouVnntHO5wSz6WpijFjHjGRc"  # Your Cloudinary API secret
)

# Pydantic model for User
class User(BaseModel):
    username: str
    password: str

# Pydantic model for Admin Login
class AdminLogin(BaseModel):
    username: str
    password: str

# Pydantic model for Vaccination Schedule
class VaccinationSchedule(BaseModel):
    month: str
    hospital: str
    location: str
    date: str
    time: str
    vaccine: str

# Pydantic model for Health Hotline
class HealthHotline(BaseModel):
    hotline_id: str
    details: dict

# Pydantic model for Infographic
class Infographic(BaseModel):
    infographic_id: str
    public_id: str  # Cloudinary public ID
    url: str        # Cloudinary URL
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
    schedules = list(vaccination_schedules_collection.find({}, {"_id": 0}))  # Exclude _id field
    if schedules:
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

# Admin Endpoints

# Endpoint to get all users
@app.get("/admin/users")
async def get_all_users():
    users = list(users_collection.find({}, {"_id": 0, "password": 0}))  # Exclude sensitive data
    if users:
        return users
    raise HTTPException(status_code=404, detail="No users found")

# Endpoint to delete a user
@app.delete("/admin/users/{username}")
async def delete_user(username: str):
    result = users_collection.delete_one({"username": username})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Vaccination Schedule Endpoints

# Endpoint to create a new vaccination schedule
@app.post("/admin/vaccination_schedules")
async def create_vaccination_schedule(schedule: VaccinationSchedule):
    result = vaccination_schedules_collection.insert_one(schedule.dict())
    if result.inserted_id:
        return {"message": "Vaccination schedule created successfully", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Failed to create vaccination schedule")

# Endpoint to update a vaccination schedule
@app.put("/admin/vaccination_schedules/{schedule_id}")
async def update_vaccination_schedule(schedule_id: str, schedule: VaccinationSchedule):
    result = vaccination_schedules_collection.update_one(
        {"_id": ObjectId(schedule_id)},
        {"$set": schedule.dict()}
    )
    if result.matched_count == 1:
        return {"message": "Vaccination schedule updated successfully"}
    raise HTTPException(status_code=404, detail="Vaccination schedule not found")

# Endpoint to delete a vaccination schedule
@app.delete("/admin/vaccination_schedules/{schedule_id}")
async def delete_vaccination_schedule(schedule_id: str):
    result = vaccination_schedules_collection.delete_one({"_id": ObjectId(schedule_id)})
    if result.deleted_count == 1:
        return {"message": "Vaccination schedule deleted successfully"}
    raise HTTPException(status_code=404, detail="Vaccination schedule not found")

# Endpoint to get all health hotlines
@app.get("/admin/health_hotlines")
async def get_all_health_hotlines():
    hotlines = list(health_hotlines_collection.find({}, {"_id": 0}))
    if hotlines:
        return hotlines
    raise HTTPException(status_code=404, detail="No health hotlines found")

# Endpoint to update a health hotline
@app.put("/admin/health_hotlines/{hotline_id}")
async def update_health_hotline(hotline_id: str, hotline: HealthHotline):
    result = health_hotlines_collection.update_one(
        {"hotline_id": hotline_id},
        {"$set": hotline.details}
    )
    if result.matched_count == 1:
        return {"message": "Health hotline updated successfully"}
    raise HTTPException(status_code=404, detail="Health hotline not found")

# Infographics Endpoints (Cloudinary Integration)

# Endpoint to upload an infographic to Cloudinary
@app.post("/admin/infographics/upload")
async def upload_infographic(file: UploadFile = File(...)):
    try:
        # Upload the file to Cloudinary
        upload_result = cloudinary.uploader.upload(file.file, folder="infographics")
        
        # Save the infographic details in MongoDB
        infographic = {
            "public_id": upload_result["public_id"],
            "url": upload_result["secure_url"]
        }
        infographics_collection.insert_one(infographic)

        return {"message": "Infographic uploaded successfully", "infographic": infographic}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get all infographics
@app.get("/admin/infographics")
async def get_all_infographics():
    infographics = list(infographics_collection.find({}, {"_id": 0}))
    if infographics:
        return infographics
    raise HTTPException(status_code=404, detail="No infographics found")

# Endpoint to delete an infographic from Cloudinary and MongoDB
@app.delete("/admin/infographics/{public_id}")
async def delete_infographic(public_id: str):
    try:
        # Delete the infographic from Cloudinary
        cloudinary.uploader.destroy(public_id)

        # Delete the infographic from MongoDB
        result = infographics_collection.delete_one({"public_id": public_id})
        if result.deleted_count == 1:
            return {"message": "Infographic deleted successfully"}
        raise HTTPException(status_code=404, detail="Infographic not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/login")
async def admin_login(admin: AdminLogin):
    # Fetch admin data from the database
    admin_data = admin_collection.find_one({"username": admin.username})
    if not admin_data:
        raise HTTPException(status_code=404, detail="Admin not found")

    # Verify the password
    if not verify_password(admin.password, admin_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Admin login successful", "username": admin.username}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)