import bcrypt
from data.data_users import DataUsers
from business.controls import ControlUserExist, ControlsValidatePassword, ControlNotFoundUser, ControlUserAndPasswordNotEmpty

class UserLogic:
    def __init__(self, username, password):
        self.username = username.lower()
        self.password = password
        self.data_users = DataUsers()

    def hash_password(self):
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, hashed):
        return bcrypt.checkpw(self.password.encode(), hashed.encode())

    def create_user(self, password2):
        chain = ControlUserAndPasswordNotEmpty(self.username, self.password)
        chain.setNext(ControlUserExist(self))
        chain.setNext(ControlsValidatePassword(self.password, password2))
        chain.handle(self.username)

        hashed = self.hash_password()
        self.data_users.add_user(self.username, hashed)

    def login_user(self):
        chain = ControlNotFoundUser(self)
        chain.handle(self.username)

        hashed = self.data_users.get_hashed_password(self.username)
        if not self.check_password(hashed):
            raise ValueError("La contraseña ingresada es incorrecta.")

        return self.username