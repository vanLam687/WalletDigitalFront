from presentation.transaction_handler import TransactionHandler

class MenuTransaction:
    def __init__(self, username):
        self.username = username

    def show(self):
        th = TransactionHandler(self.username)
        while True:
            print("\n⁞ Menú de Transacciones")
            print("1) ‟Crear cuenta”")
            print("2) ‟Depositar ARS”")
            print("3) ‟Comprar moneda”")
            print("4) ‟Vender moneda”")
            print("5) ‟Ver cuentas”")
            print("6) ‟Volver al menú principal”")
            option = input("Seleccione una opción: ").strip().upper().lower()

            if option == "1":
                volver = th.create_account()
                if volver is False:
                    break
            elif option == "2":
                volver = th.deposit_ars()
                if volver is False:
                    break
            elif option == "3":
                volver = th.buy_currency()
                if volver is False:
                    break
            elif option == "4":
                volver = th.sell_currency()
                if volver is False:
                    break
            elif option == "5":
                volver = th.show_accounts()
                if volver is False:
                    break
            elif option == "6":
                break
            else:
                print("La opción ingresada no es válida, intentalo de nuevo")