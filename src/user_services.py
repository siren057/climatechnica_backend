from user_repository import UserRepository

from user_translator import *
import bcrypt


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    async def get_by_id(self, user_id):

        return await self.repository.get_by_id(user_id)

    async def get_users(self):

        return await self.repository.get_all()

    async def create_user(self, document):

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(document["password"].encode('utf-8'), salt)

        user = User.from_request(document, hashed_password)

        result = await self.repository.create(user)

        return result

    async def update_user(self, user_id, document):

        db_user = await self.repository.get_by_id(user_id)

        if db_user is None:
            return None

        if document.get("password_hash") is not None:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(document["password"].encode('utf-8'), salt)
        else:
            hashed_password = db_user.password_hash

        db_user.update_attributes(document, hashed_password)

        await self.repository.update(user_id, db_user)

        return db_user

    async def delete_user(self, user_id):

        await self.repository.delete(user_id)
