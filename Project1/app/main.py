from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import users, contacts, auth
from app.core.config import settings
from app.presentation.json_view import JSONView  

app = FastAPI(title="Contacts API")

view = JSONView()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

@app.get("/help", tags=["meta"])
async def get_help():
    return view.response_help()
