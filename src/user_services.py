import starlette.status
from user_repository import UserRepository
import bcrypt
from user_translator import *


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    async def get_users(self):
        return await self.user_repository.get_all()

    async def create_user(self, document):
        user = User.from_request(document)
        user.password = self.hash_password(user.password)
        await self.user_repository.create(user)
        return user

    async def update_user(self, user_id, document):
        user = User.from_request(await self.user_repository.find_one(user_id))
        if not user:
            return starlette.status.HTTP_404_NOT_FOUND
        result = await self.user_repository.update(user_id, user.update_attributes(document))

        if result.modified_count >= 1:
            return User.from_request(await self.user_repository.find_one(user_id))

    async def delete_user(self, user_id):
        await self.user_repository.delete(user_id)
