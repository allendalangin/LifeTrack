# src/models/infographics_model.py
import cloudinary
import cloudinary.api

class InfographicsModel:
    def __init__(self):
        # Configure Cloudinary
        cloudinary.config(
            cloud_name="dp8qhz9w7",
            api_key="348841966416776",
            api_secret="G5OouVnntHO5wSz6WpijFjHjGRc",
            secure=True
        )

    def get_infographics(self):
        """Fetch all infographics from Cloudinary."""
        try:
            result = cloudinary.api.resources(type="upload", max_results=100)  # Fetch up to 100 images
            infographics = [{"url": resource["secure_url"], "public_id": resource["public_id"]} for resource in result["resources"]]
            return infographics
        except Exception as e:
            print(f"Error fetching infographics from Cloudinary: {e}")
            return []