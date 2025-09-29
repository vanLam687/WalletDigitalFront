from decimal import Decimal
from data.data_accounts import DataAccounts
from business.currency import Currency
from business.controls import ControlAccountExist, ControlNotFoundAccount, ControlBalance, ControlCodeCurrency, ControlArsCurrency, ControlPositiveAmount

class TransactionLogic:
    def __init__(self, username):
        self.username = username
        self.data_accounts = DataAccounts()
        self.currency = Currency()

    def create_account(self, currency):
        currency = currency.upper()
        handler = ControlCodeCurrency(currency)
        handler.setNext(ControlAccountExist(self, currency))
        handler.handle(currency)
        self.data_accounts.create_account(self.username, currency)

    def deposit_ars(self, amount):
        handler = ControlPositiveAmount(amount)
        handler.handle(amount)
        self.data_accounts.credit_account(self.username, "ARS", Decimal(amount))

    def buy_currency(self, currency_want, amount_ars):
        self.exchange("ARS", currency_want, amount_ars)

    def sell_currency(self, currency_have, amount):
        self.exchange(currency_have, "ARS", amount)

    def exchange(self, currency_have, currency_want, amount):
        currency_have = currency_have.upper()
        currency_want = currency_want.upper()

        chain = ControlCodeCurrency(currency_have)
        chain.setNext(ControlCodeCurrency(currency_want)) \
             .setNext(ControlArsCurrency(currency_have, currency_want)) \
             .setNext(ControlNotFoundAccount(self, currency_have)) \
             .setNext(ControlPositiveAmount(amount)) \
             .setNext(ControlBalance(self, currency_have, Decimal(amount)))

        chain.handle(amount)

        converted_amount = self.currency.convert(amount, currency_have, currency_want)
        self.data_accounts.debit_account(self.username, currency_have, Decimal(amount))
        self.data_accounts.credit_account(self.username, currency_want, converted_amount)

    def get_accounts(self):
        return self.data_accounts.get_accounts(self.username)