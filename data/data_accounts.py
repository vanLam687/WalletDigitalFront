from data.orm import User, Account
from decimal import Decimal
import sqlobject as SO

class DataAccounts:
    def get_user(self, username):
        try:
            return User.selectBy(username=username).getOne()
        except SO.SQLObjectNotFound:
            raise ValueError("Usuario no encontrado.")

    def create_account(self, username, currency):
        user = self.get_user(username)
        if self.account_exists(username, currency):
            raise ValueError("La cuenta ya existe.")
        Account(user=user, currency=currency, balance=Decimal("0.00"))

    def account_exists(self, username, currency):
        user = self.get_user(username)
        return Account.selectBy(user=user, currency=currency).count() > 0

    def credit_account(self, username, currency, amount):
        user = self.get_user(username)
        acc = Account.selectBy(user=user, currency=currency).getOne()
        acc.balance += amount

    def debit_account(self, username, currency, amount):
        user = self.get_user(username)
        acc = Account.selectBy(user=user, currency=currency).getOne()
        acc.balance -= amount

    def get_balance(self, username, currency):
        user = self.get_user(username)
        acc = Account.selectBy(user=user, currency=currency).getOne()
        return acc.balance

    def get_accounts(self, username):
        user = self.get_user(username)
        return {acc.currency: str(acc.balance) for acc in user.accounts}