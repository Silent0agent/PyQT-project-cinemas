from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QInputDialog, QMessageBox, QLineEdit

from config.paths import paths
from config.settings import ADMINISTRATION_KEYS


class RegistrationWindow(QWidget):
    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.setWindowIcon(QIcon(paths.get_icon('reg_icon.png')))
        self.pix = QPixmap(paths.get_background("cinema_background_1.jpeg"))
        self.setFixedSize(1000, 600)
        self.lay = QHBoxLayout(self)
        self.btn1 = QPushButton('Клиент', self)
        self.btn1.setFixedSize(300, 100)
        self.btn1.setStyleSheet("background-color: orange;border : 2px solid black;border-radius: 20px;font: bold 30px")
        self.btn1.clicked.connect(self.switch_to_client)
        self.btn2 = QPushButton('Администратор', self)
        self.btn2.setFixedSize(300, 100)
        self.btn2.setStyleSheet("background-color: orange;border : 2px solid black;border-radius: 20px;font: bold 30px")
        self.btn2.clicked.connect(self.switch_to_admin)

        self.lay.addWidget(self.btn1)
        self.lay.addWidget(self.btn2)

        self.setLayout(self.lay)

    def paintEvent(self, e):
        pix = self.pix.scaled(self.size())
        p = QPainter(self)
        p.drawPixmap(0, 0, pix)

    def switch_to_client(self):
        self.mode_return = 0
        self.switch_window.emit()

    def switch_to_admin(self):
        password, ok_pressed = QInputDialog.getText(
            self,
            "Введите ключ",
            "Ваш ключ для администрирования:",
            echo=QLineEdit.EchoMode.Password  # Скрываем ввод
        )

        if ok_pressed:
            if password in ADMINISTRATION_KEYS:
                self.mode_return = 1
                self.switch_window.emit()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Неверный ключ')
                dlg.setText("Ключа нет в списке программы")
                dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

                ok_button = dlg.button(QMessageBox.StandardButton.Ok)
                ok_button.setText("Попробовать снова")
                cancel_button = dlg.button(QMessageBox.StandardButton.Cancel)
                cancel_button.setText("Назад")

                dlg.setIcon(QMessageBox.Icon.Warning)

                # Обрабатываем результат
                if dlg.exec() == QMessageBox.StandardButton.Cancel:
                    return  # Просто закрываем окно без действий
                else:
                    self.switch_to_admin()  # Рекурсивный вызов для повторной попытки
        else:
            return