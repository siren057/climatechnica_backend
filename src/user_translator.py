from models import *


class ProfileMongoTranslator:

    def to_document(self, model: Profile) -> dict:
        return {
            "first_name": model.first_name,
            "last_name": model.last_name,
            "address": model.address
        }

    def from_document(document: dict) -> Profile:
        return Profile(**document)


class UserMongoTranslator:
    def __init__(self):
        self.profile_translator = ProfileMongoTranslator()

    def to_document(self, model) -> dict:
        return {
            "_id": model._id,
            "email": model.email,
            "password": model.password,
            "profile": self.profile_translator.to_document(model.profile),
            "city": model.city
        }

    def from_document(self, document: dict) -> User:
        return User(
            _id=str(document.get('_id')),
            email=document.get('email'),
            password=document.get("password"),
            profile=ProfileMongoTranslator.from_document(document.get("profile")),
            city=document.get("city")
        )


