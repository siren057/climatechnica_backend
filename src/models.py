class Profile:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address


class User:
    def __init__(self, email, password, profile, city):
        self.email = email
        self.password = password
        self.profile = profile
        self.city = city


class UserFromDB(User):
    def __init__(self, user_id, email, password, profile, city):
        self.user_id = user_id
        super().__init__(email, password, profile, city)



