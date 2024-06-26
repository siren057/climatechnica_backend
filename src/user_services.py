import starlette.status
from user_repository import UserRepository
from bson import ObjectId
from user_translator import *
import bcrypt


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def profile_dict(self,
                     document: dict) -> Profile:
        return Profile(**document)

    def from_dict(self,
                  document: dict) -> User:
        return User(
            _id=str(document.get('_id')),
            email=document.get('email'),
            password=document.get("password"),
            profile=self.profile_dict(document.get("profile")),
            city=document.get("city")
        )

    async def get_users(self):
        return await self.repository.get_all()

    async def create_user(self, document):
        user = self.from_dict(document)

        user._id = str(ObjectId())
        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
        await self.repository.create(user)
        return user

    async def update_user(self, user_id, document):
        user = self.from_dict(document)
        db_user = await self.repository.find_one(user_id)
        if not db_user:
            return None

        updated_profile = {
            "first_name": user.profile.first_name,
            "last_name": user.profile.last_name,
            "address": user.profile.address
        }

        updated_user = {
            "_id": db_user._id,
            "email": db_user.email,
            "password": db_user.password,
            "profile": updated_profile,
            "city": db_user.city
        }

        await self.repository.update(user_id, self.from_dict(updated_user))

        return self.from_dict(updated_user)

    async def delete_user(self, user_id):
        await self.repository.delete(user_id)
