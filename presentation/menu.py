from presentation.menu_handler import MenuHandler
from presentation.transaction_menu import MenuTransaction

class Menu:
    def menu(self):
        while True:
            print("\n⁞ Menú ")
            print("1) ‟Crear un nuevo usuario”")
            print("2) ‟Ingresar usuario”")
            print("3) ‟Salir”")
            option = input("\nSeleccione una de las opciones: ").strip().upper().lower()
            if option == "1":
                handler = MenuHandler(registration=True)
                back = handler.register()
                if not back:
                    break
            elif option == "2":
                handler = MenuHandler(registration=False)
                if handler.login():
                    mt = MenuTransaction(handler.username)
                    mt.show()
            elif option == "3":
                print("Hasta luego.")
                break
            else:
                print("La opción ingresada no es válida, intentalo de nuevo")