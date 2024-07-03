from models import *


class ProfileMongoTranslator:

    def to_document(self, model: Profile) -> dict:
        return {
            "first_name": model.first_name,
            "last_name": model.last_name,
            "address": model.address
        }

    def from_document(self, document: dict) -> Profile:
        return Profile(
            first_name=document.get("first_name"),
            last_name=document.get("last_name"),
            address=document.get("address")
        )


class UserMongoTranslator:
    def __init__(self, profile_translator: ProfileMongoTranslator):
        self.profile_translator = profile_translator

    def to_document(self, model) -> dict:
        return {
            "email": model.email,
            "password_hash": model.password_hash,
            "profile": self.profile_translator.to_document(model.profile),
            "city": model.city
        }

    def from_document(self, document) -> User:
        return User(
            user_id=str(document.get("_id")),
            email=document.get('email'),
            password_hash=document.get("password_hash"),
            profile=self.profile_translator.from_document(document.get("profile")),
            city=document.get("city")
        )


