class Profile:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address


class User:
    def __init__(self, _id, email, password, profile, city):
        self._id = _id
        self.email = email
        self.password = password
        self.profile = profile
        self.city = city




