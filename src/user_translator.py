from models import *


class ProfileMongoTranslator:


    @staticmethod
    def from_document(document: dict) -> Profile:
        return Profile(
            first_name=document.get("first_name"),
            last_name=document.get("last_name"),
            address=document.get("address")
        )

    def to_document(self: Profile) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address
        }


class UserWithIdMongoTranslator:
    @staticmethod
    def from_document(document: dict) -> UserWithID:
        return UserWithID(
            id=str(document.get("_id")),
            email=document.get('email'),
            password=document.get("password"),
            profile=ProfileMongoTranslator.from_document(document.get("profile")),
            city=document.get("city")
        )

    def to_document(self: UserWithID) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "profile": ProfileMongoTranslator.to_document(self.profile),
            "city": self.city
        }
class UserMongoTranslator:
    @staticmethod
    def from_document(document: dict) -> User:
        return User(
            email=document.get('email'),
            password=document.get("password"),
            profile=ProfileMongoTranslator.from_document(document.get("profile")),
            city=document.get("city")
        )

    def to_document(self: User) -> dict:
        return {
            "email": self.email,
            "password": self.password,
            "profile": ProfileMongoTranslator.to_document(self.profile),
            "city": self.city
        }