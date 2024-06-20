from models import *
from bson import ObjectId


class ProfileMongoTranslator(Profile):
    @staticmethod
    def from_document(document: dict):
        return Profile(
            first_name=document["first_name"],
            last_name=document["last_name"],
            address=document["address"]
        )

    def to_document(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address
        }


class UserMongoTranslator(User):
    @staticmethod
    def from_document(document: dict) -> User:
        return User(
            id=str(ObjectId(document.get("_id"))),
            email=document.get('email'),
            password=document.get("password"),
            profile=ProfileMongoTranslator.from_document(document.get("profile")),
            city=document.get("city")
        )

    def to_document(self: User) -> dict:
        return {
            "id": self.id or None,
            "email": self.email or None,
            "password": self.password or None,
            "profile": ProfileMongoTranslator.to_document(self.profile) or None,
            "city": self.city or None
        }
