from user_repository import UserRepository

from user_translator import *
import bcrypt


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def validate_document(self, document):
        try:
            email = document["email"]
            password = document["password"]
            profile = document["profile"]
            city = document["city"]
        except KeyError as e:
            raise e
        return True

    async def get_by_id(self, user_id):

        return await self.repository.get_by_id(user_id)

    async def get_users(self):

        return await self.repository.get_all()

    async def create_user(self, document):

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(document["password"].encode('utf-8'), salt)
        if self.validate_document(document):
            user = User.from_request(document)
            user.password_hash = hashed_password
            user.id = await self.repository.create(user)
            return user
        else:
            return None

    async def update_user(self, user_id, document):

        db_user = await self.repository.get_by_id(user_id)

        if db_user is None:
            return None

        db_user.update_attributes(document)

        await self.repository.update(user_id, db_user)

        return db_user

    async def delete_user(self, user_id):

        await self.repository.delete(user_id)
