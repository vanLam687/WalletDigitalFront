import time
from decimal import Decimal, InvalidOperation
from business.transaction_logic import TransactionLogic

class TransactionHandler:
    def __init__(self, username):
        self.username = username
        self.logic = TransactionLogic(username)

    def again(self):
        while True:
            opcion = input("\n¿Quieres intentarlo nuevamente? s/n: ").strip().upper().lower()
            if opcion == 's':
                return True
            elif opcion == 'n':
                return False
            else:
                print("Ingresa s para sí o n para no.")

    def continuee(self):
        while True:
            opcion = input("\n¿Quieres volver al menú? s/n: ").strip().upper().lower()
            if opcion == 's':
                return True
            elif opcion == 'n':
                print("\nAdiós.")
                return False
            else:
                print("Ingresa s para sí o n para no.")
                
    def confirm_time(self, mensaje="¿Seguro que quieres realizar esta operación? s/n:", time_limit=120):
        print("Tienes ", time_limit, "segundos para confirmar.")
        tstart = time.time()
        rta = input(mensaje).strip().upper().lower()
        if (time.time() - tstart) > time_limit:
            print("Tiempo de espera excedido. La operación ha sido cancelada.")
            return False
        if rta == 's':
            return True
        else:
            print("Cancelaste la operación.")
            return False

    def create_account(self):
        while True:
            currency = input("Ingrese la moneda: ").strip().upper().lower()
            if len(currency) != 3 or not currency.isalpha():
                print("Ingrese un código de moneda que sea válido.")
                if not self.again():
                    return True 
                continue
            try:
                self.logic.create_account(currency)
                print("Su cuenta ha sido creada con éxito.")
                return self.continuee()
            except ValueError as e:
                print("ERROR:  ", e)
                if not self.again():
                    return True

    def deposit_ars(self):
        while True:
            entrada = input("Ingrese el monto en ars a depositar: ").strip().upper().lower()
            try:
                amount = Decimal(entrada)
                if amount <= 0:
                    print("El depósito debe ser mayor a 0.")
                    if not self.again():
                        return True
                    continue
                self.logic.deposit_ars(amount)
                print("Su depósito ha sido realizado con éxito.")
                return self.continuee()
            except InvalidOperation:
                print("El valor ingresado no es un número válido.")
                if not self.again():
                    return True
            except ValueError as e:
                print("ERROR: ", e)
                if not self.again():
                    return True

    def buy_currency(self):
        while True:
            target = input("Ingrese la moneda a comprar: ").strip().upper().lower()
            if len(target) != 3 or not target.isalpha():
                print("Ingrese un código de moneda válido.") 
                if not self.again():
                    return True
                continue

            entrada = input("Ingrese el monto en ars para comprar: ").strip().upper().lower()
            try:
                amount = Decimal(entrada)
                if amount <= 0:
                    print("El monto debe ser mayor a 0.")
                    if not self.again():
                        return True
                    continue
            except InvalidOperation:
                print("El valor ingresado no es un número válido.")
                if not self.again():
                    return True
                continue

            if not self.confirm_time():
                return self.continuee()

            try:
                self.logic.buy_currency(target, amount)
                print("Compra realizada con éxito.")
            except ValueError as e:
                print("ERROR: ", e)
                if not self.again():
                    return True
                continue

            return self.continuee()

    def sell_currency(self):
        while True:
            origin = input("Ingrese la moneda a vender: ").strip().upper().lower()

            if len(origin) != 3 or not origin.isalpha():
                print("Ingrese un código de moneda válido.")
                if not self.again():
                    return True
                continue

            if origin == "ARS":
                print("No puedes vender ars. Solo puedes vender monedas extranjeras para obtener ars.")
                if not self.again():
                    return True
                continue

            entrada = input("Ingrese el monto a vender: ").strip().upper().lower()
            try:
                amount = Decimal(entrada)
                if amount <= 0:
                    print("El monto debe ser mayor a 0.")
                    if not self.again():
                        return True
                    continue
            except InvalidOperation:
                print("El valor ingresado no es un número válido.")
                if not self.again():
                    return True
                continue

            if not self.confirm_time():
                return self.continuee()

            try:
                self.logic.sell_currency(origin, amount)
                print("Venta realizada con éxito.")
            except ValueError as e:
                print(f"ERROR:  ", e)
                if not self.again():
                    return True
                continue

            return self.continuee()

    def show_accounts(self):
        accounts = self.logic.get_accounts()
        print("\n⁞ Cuentas de " + self.username + ":")
        for moneda, saldo in accounts.items():
            print(moneda + " : " + saldo)
        return self.continuee()