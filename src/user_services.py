from user_repository import UserRepository

from user_translator import *
import bcrypt


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    async def get_by_id(self, user_id):
        return await self.repository.find_by_id(user_id)

    async def get_users(self):
        return await self.repository.get_all()

    async def create_user(self, document):
        user = User.from_request(document)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
        user.password = hashed_password

        result = await self.repository.create(user)

        return result

    async def update_user(self, user_id, document):
        user, user.user_id = User.from_request(document), user_id

        db_user = await self.repository.find_by_id(user_id)

        if not db_user:
            return None

        user.update_attributes(db_user, ["password", "city"])

        await self.repository.update(user_id, user)

        return user

    async def delete_user(self, user_id):
        await self.repository.delete(user_id)
