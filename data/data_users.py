from data.orm import User, Account
from sqlobject import SQLObjectNotFound
from decimal import Decimal

class DataUsers:
    def read(self, username):
        try:
            return User.selectBy(username=username).getOne()
        except SQLObjectNotFound:
            raise ValueError("Usuario no encontrado.")

    def user_exists(self, username):
        return User.selectBy(username=username).count() > 0

    def add_user(self, username, hashed_password):
        if self.user_exists(username):
            raise ValueError("El usuario ya existe.")
        user = User(username=username, pwd=hashed_password)
        Account(user=user, currency="ARS", balance=Decimal("0.00"))

    def get_hashed_password(self, username):
        try:
            return self.read(username).pwd
        except SQLObjectNotFound:
            return None