from PyQt6.QtSql import QSqlTableModel, QSqlDatabase
from PyQt6.QtWidgets import QWidget, QPushButton, QTableView, QVBoxLayout, QTimeEdit, QCalendarWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon

from config.paths import paths
from config.settings import DATABASE_PATH


class ShowCinemas(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(str(DATABASE_PATH))
        db.open()
        view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('Cinemas')
        model.select()
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)

        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Кинотеатры')


class ShowHalls(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(str(DATABASE_PATH))
        db.open()
        view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('Halls')
        model.select()
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)

        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Залы')


class ShowSessions(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(str(DATABASE_PATH))
        db.open()
        view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('Sessions')
        model.select()
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)

        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Сеансы')


class ShowFilms(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(str(DATABASE_PATH))
        db.open()
        view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('Films')
        model.select()
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)

        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Фильмы')


class DateChoose(QWidget):
    upd_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.main_lay = QVBoxLayout(self)
        self.setWindowTitle('Выбрать время начала')
        self.setWindowIcon(QIcon(paths.get_icon('calendar_icon')))
        self.timeEdit = QTimeEdit(self)
        self.calendarWidget = QCalendarWidget(self)
        self.addTimeBtn = QPushButton('Выбрать время', self)
        self.addTimeBtn.clicked.connect(self.add_time)

        self.main_lay.addWidget(self.timeEdit)
        self.main_lay.addWidget(self.calendarWidget)
        self.main_lay.addWidget(self.addTimeBtn)

        self.setLayout(self.main_lay)

    def add_time(self):
        date = self.calendarWidget.selectedDate()
        time = self.timeEdit.time()
        self.ret = (f'{str(date.year()).zfill(4)}-{str(date.month()).zfill(2)}-{str(date.day()).zfill(2)}'
                    f' {str(time.hour()).zfill(2)}:{str(time.minute()).zfill(2)}:{str(time.second()).zfill(2)}')
        self.upd_window.emit()
