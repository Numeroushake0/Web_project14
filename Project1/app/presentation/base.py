from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseView(ABC):
    @abstractmethod
    def show_help(self) -> str:
        pass

    @abstractmethod
    def show_contacts(self, contacts: List[Dict[str, Any]]) -> str:
        pass

    @abstractmethod
    def show_message(self, message: str) -> str:
        pass
