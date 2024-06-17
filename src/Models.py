class Profile:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address


class UserCreate:
    def __init__(self, email, password, profile, city):
        self.email = email
        self.password = password
        self.profile = profile
        self.city = city


class User(UserCreate):
    def __init__(self, user_id: str, email: str, password: str, profile: dict, city: str):
        super().__init__(email, password, profile, city)
        self.user_id = user_id

    @staticmethod
    def parseDTO(UserDTO):
        return User(str(UserDTO.user_id), UserDTO.email, UserDTO.password,
                    UserDTO.profile, UserDTO.city)
