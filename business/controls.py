from business.cor import BaseHandler
from business.currency import Currency
from decimal import Decimal

class ControlsValidatePassword(BaseHandler):
    def __init__(self, password, password2):
        super().__init__()
        self.password = password
        self.password2 = password2

    def handle(self, password):
        if self.password != self.password2:
            raise ValueError("Las contraseñas que ingresaste no coinciden.")
        return super().handle(password)

class ControlUserExist(BaseHandler):
    def __init__(self, user_logic):
        super().__init__()
        self.user_logic = user_logic

    def handle(self, users):
        if self.user_logic.data_users.user_exists(self.user_logic.username):
            raise ValueError("El usuario que ingresaste ya existe.")
        return super().handle(users)

class ControlUserAndPasswordNotEmpty(BaseHandler):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def handle(self, param):
        if not self.username or self.username.strip() == "":
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if not self.password or self.password.strip() == "":
            raise ValueError("La contraseña no puede estar vacía.")
        return super().handle(param)

class ControlNotFoundUser(BaseHandler):
    def __init__(self, user_logic):
        super().__init__()
        self.user_logic = user_logic

    def handle(self, users):
        if not self.user_logic.data_users.user_exists(self.user_logic.username):
            raise ValueError("El usuario que ingresaste no existe.")
        return super().handle(users)

class ControlAccountExist(BaseHandler):
    def __init__(self, logic, currency):
        super().__init__()
        self.logic = logic
        self.currency = currency

    def handle(self, users):
        if self.logic.data_accounts.account_exists(self.logic.username, self.currency):
            raise ValueError("La cuenta que ingresaste ya existe.")
        return super().handle(users)

class ControlNotFoundAccount(BaseHandler):
    def __init__(self, logic, currency):
        super().__init__()
        self.logic = logic
        self.currency = currency

    def handle(self, account):
        if not self.logic.data_accounts.account_exists(self.logic.username, self.currency):
            raise ValueError("No tienes una cuenta en " + self.currency + ".")
        return super().handle(account)

class ControlBalance(BaseHandler):
    def __init__(self, logic, currency, amount):
        super().__init__()
        self.logic = logic
        self.currency = currency
        self.amount = amount

    def handle(self, balance):
        saldo = self.logic.data_accounts.get_balance(self.logic.username, self.currency)
        if saldo < self.amount:
            raise ValueError("tu saldo es insuficiente.")
        return super().handle(balance)

class ControlCodeCurrency(BaseHandler):
    def __init__(self, currency_code):
        super().__init__()
        self.currency = currency_code.upper()
        self.valid = Currency()

    def handle(self, code):
        if self.currency not in self.valid.list_currencies():
            raise ValueError("La moneda ingresada no es válida.")
        return super().handle(code)

class ControlArsCurrency(BaseHandler):
    def __init__(self, currency_have, currency_want):
        super().__init__()
        self.currency_have = currency_have.upper()
        self.currency_want = currency_want.upper()

    def handle(self, currency):
        if self.currency_have == self.currency_want:
            raise ValueError("No podes convertir la misma moneda")
        return super().handle(currency)

class ControlPositiveAmount(BaseHandler):
    def __init__(self, amount):
        super().__init__()
        self.amount = Decimal(amount)

    def handle(self, amount):
        if self.amount <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return super().handle(amount)