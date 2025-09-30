from PyQt6.QtWidgets import QWidget, QMessageBox, QMainWindow, QDialog
from presentation.screens.login import Ui_Form as LoginUI
from presentation.screens.register import Ui_Form as RegisterUI
from presentation.screens.menuTransacciones import Ui_MainWindow as TransactionUI
from business.users_logic import UserLogic
from presentation.transaction_menu import TransactionWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = LoginUI()
        self.ui.setupUi(self)
        
        self.ui.btnRegistro.clicked.connect(self.open_register)
        self.ui.btnIngresar.clicked.connect(self.login)
        self.ui.lineContra.setEchoMode(self.ui.lineContra.EchoMode.Password)

    def open_register(self):
        self.register_window = RegisterWindow()
        res = self.register_window.exec()
        if res == QDialog.DialogCode.Accepted:
            pass

    def login(self):
        username = self.ui.lineNameUser.text().strip().lower()
        password = self.ui.lineContra.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
            
        try:
            logic = UserLogic(username, password)
            logic.login_user()
            self.open_transaction_menu(username)
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"ERROR: {str(e)}")

    def open_transaction_menu(self, username):
        self.transaction_window = TransactionWindow(username)
        self.transaction_window.show()
        self.hide()

class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = RegisterUI()
        self.ui.setupUi(self)
        
        self.ui.btnRegistrarse.clicked.connect(self.register)
        self.ui.lineContraReg.setEchoMode(self.ui.lineContraReg.EchoMode.Password)
        self.ui.lineContraReg2.setEchoMode(self.ui.lineContraReg2.EchoMode.Password)
        
    def register(self):
        username = self.ui.lineNameUserReg.text().strip().lower()
        password = self.ui.lineContraReg.text()
        password2 = self.ui.lineContraReg2.text()
        
        if not username or not password or not password2:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
            
        try:
            logic = UserLogic(username, password)
            logic.create_user(password2)
            QMessageBox.information(self, "Éxito", "Registro exitoso")
            self.accept()
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"ERROR: {str(e)}")