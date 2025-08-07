from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import ContactCreate, ContactOut, ContactUpdate
from app.crud import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
)
from slowapi.util import get_remote_address
from slowapi import Limiter
from app.presentation.json_view import JSONView  

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
view = JSONView()  

@router.get("/", response_model=dict)
async def read_contacts(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contacts = await get_contacts(db, current_user.id)
    return view.response_contacts([contact.dict() for contact in contacts])


@router.post(
    "/",
    response_model=dict,
    dependencies=[Depends(limiter.limit("5/minute"))]
)
async def create_new_contact(
    request: Request,
    contact_in: ContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = await create_contact(db, current_user.id, contact_in)
    return view.response_contacts([contact.dict()])


@router.get("/{contact_id}", response_model=dict)
async def read_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = await get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return view.response_contacts([contact.dict()])


@router.put("/{contact_id}", response_model=dict)
async def update_existing_contact(
    contact_id: int,
    contact_in: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = await get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    updated_contact = await update_contact(db, contact, contact_in)
    return view.response_contacts([updated_contact.dict()])


@router.delete("/{contact_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_existing_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = await get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    await delete_contact(db, contact)
    return view.response_message(f"Contact with id={contact_id} deleted successfully.")

