from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str] = Field(min_length=6)
    is_active: Optional[bool]
    is_verified: Optional[bool]

class UserOut(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    birthday: Optional[datetime]

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    birthday: Optional[datetime]

class ContactOut(ContactBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True
