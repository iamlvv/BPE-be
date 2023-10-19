import cloudinary
import json

# ==============================
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

load_dotenv()
import os

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True,
)
# Set your Cloudinary credentials
# ==============================


# Import the Cloudinary libraries


# Import to format the JSON responses
# ==============================


# Set configuration parameter: return "https" URLs by setting secure=True
# ==============================
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
print(
    "****1. Set up and configure the SDK:****\nCredentials: ",
    config.cloud_name,
    config.api_key,
    "\n",
)
