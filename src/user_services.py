import starlette.status

from user_repository import UserRepository
import bcrypt
from user_translator import *


class UserServices:
    user_repository = UserRepository()

    def profile_document_to_class(self, document: dict) -> Profile:
        return Profile(
            first_name=document.get("first_name"),
            last_name=document.get("last_name"),
            address=document.get("address")
        )

    def user_document_to_class(self, document: dict) -> User:
        return User(
            password=document.get("password"),
            email=document.get("email"),
            profile=self.profile_document_to_class(document.get("profile")),
            city=document.get("city")
        )

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    async def get_users(self):
        return await self.user_repository.get()

    async def create_user(self, document):
        user = self.user_document_to_class(document)
        user.password = self.hash_password(user.password)
        await self.user_repository.create(user)
        return starlette.status.HTTP_201_CREATED

    async def update_user(self, id, document):
        user = await self.user_repository.find_one(id)
        if not user:
            return starlette.status.HTTP_404_NOT_FOUND
        document = self.user_document_to_class(document)
        document.password = self.user_document_to_class(user).password
        return await self.user_repository.update(id, document)

    async def delete_user(self, id):
        await self.user_repository.delete(id)
        return
