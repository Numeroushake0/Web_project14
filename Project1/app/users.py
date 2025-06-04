from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import UserOut, UserUpdate
from app.crud import update_user
from app.services.cloudinary_service import upload_avatar_to_cloudinary

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await update_user(db, current_user, user_update)
    return user

@router.post("/me/avatar", response_model=UserOut)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type")
    avatar_url = await upload_avatar_to_cloudinary(file)
    current_user.avatar_url = avatar_url
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user
