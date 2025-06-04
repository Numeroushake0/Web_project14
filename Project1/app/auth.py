from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.schemas import UserCreate, UserOut
from app.models import User
from app.crud import get_user_by_email, create_user, update_user
from app.dependencies import get_db
from app.services.email_service import send_verification_email, send_reset_password_email
from app.core.config import settings
from pydantic import EmailStr

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user_in.password)
    user = await create_user(db, user_in, hashed_password)
    background_tasks.add_task(send_verification_email, user.email, user.id)
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-email")
async def verify_email(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        return {"message": "Email already verified"}
    user.is_verified = True
    db.add(user)
    await db.commit()
    return {"message": "Email verified successfully"}

@router.post("/reset-password-request")
async def reset_password_request(email: EmailStr, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email)
    if user:
        background_tasks.add_task(send_reset_password_email, user.email, user.id)
    return {"message": "If an account with that email exists, a reset link has been sent."}

@router.post("/reset-password")
async def reset_password(user_id: int, new_password: str, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    await db.commit()
    return {"message": "Password updated successfully"}
