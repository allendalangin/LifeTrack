import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = "dp8qhz9w7", 
    api_key = "348841966416776", 
    api_secret = "G5OouVnntHO5wSz6WpijFjHjGRc", # Click 'View API Keys' above to copy your API secret
    secure=True
)

# Upload an image
upload_result = cloudinary.uploader.upload("C:/Users/allen/Downloads/MPOX.jpg",
                                           public_id="MPOX")
print("Uploaded Image URL:", upload_result["secure_url"])

# Optimize delivery by applying auto-format and auto-quality
optimize_url, _ = cloudinary_url("MPOX", fetch_format="auto", quality="auto")
print("Optimized Image URL:", optimize_url)
