from .base import BaseView
from typing import List, Dict, Any


class JSONView(BaseView):
    def response_message(self, message: str) -> Dict[str, str]:
        return {"message": message}

    def response_contacts(self, contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"contacts": contacts, "count": len(contacts)}

    def response_help(self) -> Dict[str, Any]:
        return {
            "commands": [
                {"method": "POST", "path": "/auth/signup", "description": "Register new user"},
                {"method": "POST", "path": "/auth/login", "description": "Get access token"},
                {"method": "GET", "path": "/contacts", "description": "List contacts"},
                {"method": "POST", "path": "/contacts", "description": "Create contact"},
                {"method": "GET", "path": "/users/me", "description": "Get current user"},
            ]
        }
