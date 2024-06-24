from typing import Optional, Dict


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

    def update_attributes(self, update_data: Dict[str, Optional[str]]):
        return self
