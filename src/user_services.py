
from user_repository import UserRepository

from user_translator import *
import bcrypt


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    @staticmethod
    def profile_from_dict(
            document: dict) -> Profile:
        return Profile(
            first_name=document.get("first_name"),
            last_name=document.get("last_name"),
            address=document.get("address")
        )

    @staticmethod
    def user_from_dict(document: dict) -> User:
        return User(
            email=document.get('email'),
            password=document.get("password"),
            profile=UsersService.profile_from_dict(document.get("profile")),
            city=document.get("city")
        )

    async def get_users(self):
        return await self.repository.get_all()

    async def create_user(self, document):

        user = self.user_from_dict(document)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
        user.password = hashed_password

        result = await self.repository.create(user)

        return result

    async def update_user(self, user_id, document):

        user = self.user_from_dict(document)
        db_user = await self.repository.find_one(user_id)

        if not db_user:
            return None

        if user.password:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
            user.password = hashed_password
        else:
            user.password = db_user.password

        await self.repository.update(user_id, user)

        return user

    async def delete_user(self, user_id):
        db_user = self.repository.find_one(user_id)
        await self.repository.delete(user_id)

        return db_user
