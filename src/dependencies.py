from user_repository import UserRepository
from user_services import UsersService
from user_translator import UserMongoTranslator

user_mongo_translator = UserMongoTranslator()

users_repository = UserRepository(db_url="mongodb://localhost:27017", db_name="test_database", translator=user_mongo_translator)

users_service = UsersService(users_repository)

