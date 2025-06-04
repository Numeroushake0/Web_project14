import unittest
from app.schemas import ContactCreate
from app.models import Contact

class TestContactModel(unittest.TestCase):
    def test_contact_fields(self):
        contact = Contact(name="Ivan", email="ivan@example.com", phone="123456")
        self.assertEqual(contact.name, "Ivan")
        self.assertEqual(contact.email, "ivan@example.com")
