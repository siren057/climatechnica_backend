class Profile:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address


class User:
    def __init__(self, id,  email, password, profile, city):
        self.id = id or None
        self.email = email
        self.password = password
        self.profile = profile
        self.city = city


