from user_repository import UserRepository
from user_services import UsersService
from user_translator import UserMongoTranslator, ProfileMongoTranslator
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["test_database"]

profile_mongo_translator = ProfileMongoTranslator()

user_mongo_translator = UserMongoTranslator(profile_mongo_translator)

users_repository = UserRepository(db, translator=user_mongo_translator)

users_service = UsersService(users_repository)
