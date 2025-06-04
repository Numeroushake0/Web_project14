import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

async def upload_avatar_to_cloudinary(file: UploadFile) -> str:
    file_content = await file.read()
    upload_result = cloudinary.uploader.upload(
        file_content,
        folder="avatars",
        resource_type="image"
    )
    return upload_result.get("secure_url")
