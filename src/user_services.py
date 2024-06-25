import starlette.status
from user_repository import UserRepository

from user_translator import *


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_users(self):
        return await self.user_repository.get_all()

    async def create_user(self, document):
        user = User.from_request(document)
        user.hash_password()
        await self.user_repository.create(user)
        return user

    async def update_user(self, user_id, document):
        user = User.from_request(await self.user_repository.find_one(user_id))
        if not user:
            return starlette.status.HTTP_404_NOT_FOUND
        old_password = user.password
        user.update_attributes(document)
        if user.password != old_password:
            user.hash_password()
        await self.user_repository.update(user_id, user)

        return User.from_request(await self.user_repository.find_one(user_id))

    async def delete_user(self, user_id):
        await self.user_repository.delete(user_id)
