from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox
from presentation.screens.menuTransacciones import Ui_MainWindow as TransactionUI
from presentation.screens.CrearCuenta import Ui_Dialog as CrearCuentaUI
from presentation.screens.DepositarArs import Ui_Dialog as DepositarArsUI
from business.transaction_logic import TransactionLogic
from decimal import Decimal

class TransactionWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.ui = TransactionUI()
        self.ui.setupUi(self)
        self.username = username
        self.logic = TransactionLogic(username)
        
        self.setWindowTitle(f"Menú de Transacciones - {self.username}")
        
        self.ui.btnCrearCuenta.clicked.connect(self.crear_cuenta)
        self.ui.btnDepositar.clicked.connect(self.depositar_ars)

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

    def depositar_ars(self):
        dialog = DepositarArsDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            monto = dialog.get_monto()
            if monto:
                try:
                    monto_decimal = Decimal(str(monto))
                    if monto_decimal <= 0:
                        QMessageBox.warning(self, "Error", "El monto debe ser mayor a 0")
                        return
                    
                    self.logic.deposit_ars(monto_decimal)
                    QMessageBox.information(self, "Éxito", f"Depósito de ${monto} ARS realizado exitosamente")
                except ValueError as e:
                    QMessageBox.critical(self, "Error", f"ERROR: {str(e)}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")


class CrearCuentaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = CrearCuentaUI()
        self.ui.setupUi(self)
        
    def get_moneda(self):
        return self.ui.lineCodMonedaIngresar.text().strip().upper()


class DepositarArsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = DepositarArsUI()
        self.ui.setupUi(self)
        
    def get_monto(self):
        return self.ui.lineArsDepositar.text().strip()