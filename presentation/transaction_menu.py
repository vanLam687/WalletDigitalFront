from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox
from presentation.screens.menuTransacciones import Ui_MainWindow as TransactionUI
from presentation.screens.CrearCuenta import Ui_Dialog as CrearCuentaUI
from business.transaction_logic import TransactionLogic

class TransactionWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.ui = TransactionUI()
        self.ui.setupUi(self)
        self.username = username
        self.logic = TransactionLogic(username)
        
        self.setWindowTitle(f"Menú de Transacciones - {self.username}")
        
        self.ui.btnCrearCuenta.clicked.connect(self.crear_cuenta)

    def crear_cuenta(self):
        dialog = CrearCuentaDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            moneda = dialog.get_moneda()
            if moneda:
                if len(moneda) != 3 or not moneda.isalpha():
                    QMessageBox.warning(self, "Error", "El código de moneda debe tener exactamente 3 letras")
                    return
                    
                try:
                    self.logic.create_account(moneda)
                    QMessageBox.information(self, "Éxito", f"Cuenta en {moneda} creada exitosamente")
                except ValueError as e:
                    QMessageBox.critical(self, "Error", f"ERROR: {str(e)}")

class CrearCuentaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = CrearCuentaUI()
        self.ui.setupUi(self)
        
    def get_moneda(self):
        return self.ui.lineCodMonedaIngresar.text().strip().upper()