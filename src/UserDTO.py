
class UserDTO:
    def __init__(self, model):
        self.user_id = model["_id"]
        self.email = model['email']
        self.password = model["password"]
        self.profile = model["profile"]
        self.city = model["city"]
