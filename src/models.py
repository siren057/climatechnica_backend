class Profile:
    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    @staticmethod
    def from_request(
            document: dict):
        return Profile(
            first_name=document.get("first_name"),
            last_name=document.get("last_name"),
            address=document.get("address")
        )


class User:
    def __init__(self, user_id, email, password, profile, city):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.profile = profile
        self.city = city

    @staticmethod
    def from_request(document: dict):
        return User(
            user_id=document.get("_id"),
            email=document.get('email'),
            password=document.get("password"),
            profile=Profile.from_request(document.get("profile")),
            city=document.get("city")
        )

    def update_attributes(self, user, protected_attributes):
        return self
