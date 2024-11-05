

class RolesService:
    def __init__(self, user):
        self.user = user

    def is_admin(self):
        return self.user.is_admin

    def is_user(self):
        return self.user.is_user

    def create_role(self, data: dict):
        pass