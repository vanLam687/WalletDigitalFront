import pwinput
from business.users_logic import UserLogic

class MenuHandler:
    def __init__(self, registration=False):
        self.username = input("Nombre de usuario: ").strip().upper().lower()
        self.password = pwinput.pwinput("Contraseña: ", mask="•")
        self.password2 = None
        if registration:
            self.password2 = pwinput.pwinput("Reingrese la contraseña: ", mask="•")

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
                
    def register(self):
        logic = UserLogic(self.username, self.password)
        try:
            logic.create_user(self.password2)
            print("\nRegistro exitoso.")
            return self.continuee()
        except ValueError as e:
            print("ERROR:  ", e)
            if self.again():
                self.__init__(registration=True)
                return self.register()
            return True

    def login(self):
        logic = UserLogic(self.username, self.password)
        try:
            logic.login_user()
            print(f"\nBienvenido/a, {self.username}")
            return True
        except ValueError as e:
            print("ERROR: ", e)
            if self.again():
                self.__init__(registration=False)
                return self.login()
            return False