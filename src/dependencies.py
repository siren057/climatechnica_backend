from user_repository import UserRepository
from user_services import UsersService


def provide_user_repository() -> UserRepository:
    return UserRepository(db_url="mongodb://localhost:27017", db_name="test_database")


def provide_user_service() -> UsersService:
    user_repository = provide_user_repository()
    return UsersService(user_repository)
