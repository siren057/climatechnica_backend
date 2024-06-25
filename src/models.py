from typing import Optional, Dict
import bcrypt


class Profile:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    @classmethod
    def from_request(cls, document: dict):
        return Profile(
            first_name=document.get("first_name"),
            last_name=document.get("last_name"),
            address=document.get("address")
        )

    def update_attributes(self, updates):
        for key, value in updates.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)


class User:
    def __init__(self, email: str, password: str, profile: object, city: str, id: Optional[str]):
        self.id = id
        self.email = email
        self.password = password
        self.profile = profile
        self.city = city

    @classmethod
    def from_request(cls, document: dict):
        return User(
            id=str(document.get('_id')),
            email=document.get('email'),
            password=document.get("password"),
            profile=Profile.from_request(document.get("profile")),
            city=document.get("city")
        )

    def hash_password(self):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), salt)

    def update_attributes(self, update_data: Dict[str, Optional[str]]):
        for key, value in update_data.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if isinstance(attr, (Profile, User)) and isinstance(value, dict):
                    attr.update_attributes(value)
                elif value is not None:
                    setattr(self, key, value)
