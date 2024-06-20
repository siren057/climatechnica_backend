import starlette.status

from models import User
from user_repository import UserRepository
import bcrypt
from user_translator import *


class UserServices:
    def __init__(self):
        self.user_repository = UserRepository()

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    async def get_user():
        ls = set()
        for i in await UserRepository.get():
            ls.add(UserMongoTranslator.from_document(i))
        return ls

    @staticmethod
    def update_user_attributes(user: User, document: dict):
        if 'name' in document:
            user.name = document['name']
        if 'email' in document:
            user.email = document['email']
        if 'password' in document:
            user.password = document['password']
        if 'age' in document:
            user.age = document['age']

    async def create_user(self, document):
        user = UserMongoTranslator.from_document(document)
        user.password = self.hash_password(user.password)
        await UserRepository.create(UserMongoTranslator.to_document(user))
        return starlette.status.HTTP_201_CREATED

    async def update_user(self, id, document):
        candidate = await UserRepository.find_one(id)
        if not candidate:
            return starlette.status.HTTP_400_BAD_REQUEST
        user_obj = UserMongoTranslator.from_document(candidate)
        self.update_user_attributes(user_obj, document)

        await UserRepository.update(id, UserMongoTranslator.to_document(user_obj))

        return starlette.status.HTTP_201_CREATED

    async def delete_user(self, id):
        candidate = await UserRepository.find_one(id)
        if not candidate:
            return starlette.status.HTTP_400_BAD_REQUEST
        await UserRepository.delete(id)
        return starlette.status.HTTP_200_OK
