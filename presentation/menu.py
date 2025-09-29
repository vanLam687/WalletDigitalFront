from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox
from presentation.screens.login import Ui_Form as LoginUI
from presentation.screens.register import Ui_Form as RegisterUI
from business.users_logic import UserLogic

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LoginUI()
        self.ui.setupUi(self)
        
        self.ui.btnRegistro.clicked.connect(self.open_register)
        
    def open_register(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()

class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = RegisterUI()
        self.ui.setupUi(self)
        self.parent_window = parent
        
        self.ui.btnRegistrarse.clicked.connect(self.register)
        
        self.ui.lineContraReg.setEchoMode(self.ui.lineContraReg.EchoMode.Password)
        self.ui.lineContraReg2.setEchoMode(self.ui.lineContraReg2.EchoMode.Password)
    
    def ask_retry(self, message):
        reply = QMessageBox.question(self, "Reintentar", message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return reply == QMessageBox.StandardButton.Yes

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
        
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
            
            self.close()
            if self.parent_window:
                self.parent_window.show()
            
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"ERROR: {str(e)}")
            if self.ask_retry("¿Quieres intentarlo nuevamente?"):
                self.ui.lineNameUserReg.clear()
                self.ui.lineContraReg.clear()
                self.ui.lineContraReg2.clear()
                self.ui.lineNameUserReg.setFocus()