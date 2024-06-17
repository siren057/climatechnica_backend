from Models import User
from UserRepository import UserRepository
import bcrypt


class UserServices:
    def __init__(self):
        self.user_repository = UserRepository()

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    async def get_user(self, user_id) -> User:
        return User.parseDTO(await self.user_repository.get_user_by_id(user_id))

    async def create_user(self, user_json):
        user_json["password"] = self.hash_password(user_json["password"])
        try:
            return User.parseDTO(await self.user_repository.create_user(user_json))
        except ValueError as e:
            return {"error": str(e)}

    async def update_user(self, user_id: str, user_json):
        user_json["password"] = self.hash_password(user_json["password"])
        try:
            return User.parseDTO(await self.user_repository.update_user_by_id(user_id, user_json))
        except ValueError as e:
            return {"error": str(e)}

    async def delete_user(self, user_id):
        return await self.user_repository.delete_user_by_id(user_id)
