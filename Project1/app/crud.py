from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, Contact
from app.schemas import UserCreate, ContactCreate, UserUpdate, ContactUpdate
from typing import List, Optional

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    return await db.get(User, user_id)

async def create_user(db: AsyncSession, user_in: UserCreate, hashed_password: str) -> User:
    user = User(email=user_in.email, hashed_password=hashed_password, is_active=True, is_verified=False)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_contacts(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[Contact]:
    result = await db.execute(select(Contact).where(Contact.owner_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_contact(db: AsyncSession, contact_id: int, user_id: int) -> Optional[Contact]:
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.owner_id == user_id))
    return result.scalars().first()

async def create_contact(db: AsyncSession, user_id: int, contact_in: ContactCreate) -> Contact:
    contact = Contact(**contact_in.dict(), owner_id=user_id)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def update_contact(db: AsyncSession, contact: Contact, contact_in: ContactUpdate) -> Contact:
    for field, value in contact_in.dict(exclude_unset=True).items():
        setattr(contact, field, value)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def delete_contact(db: AsyncSession, contact: Contact) -> None:
    await db.delete(contact)
    await db.commit()
