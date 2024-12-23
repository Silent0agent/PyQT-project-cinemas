import sqlite3
import sys

from PyQt6.QtSql import QSqlTableModel, QSqlDatabase
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QApplication, QTableView, QFileDialog, \
    QLabel, QGridLayout, QInputDialog, QVBoxLayout, QMessageBox, QTimeEdit, QCalendarWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6 import uic


# В коде закомментированы все строки, связанные с блокировкой администрирования
# Список ключей для входа в администрирования
# SPECIAL_KEYS = ['gas', 'kerg', 'bserthfdv', '234lsjdfp']


class Registration(QWidget):
    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.setWindowIcon(QIcon('res\\pictures\\icons\\reg_icon.png'))
        self.pix = QPixmap("res\\pictures\\backgrounds\\cinema_background_1.jpeg")
        self.setFixedSize(1000, 600)
        self.lay = QHBoxLayout(self)
        self.btn1 = QPushButton('Клиент', self)
        self.btn1.setFixedSize(300, 100)
        self.btn1.setStyleSheet("background-color: orange;border : 2px solid black;border-radius: 20px;font: bold 30px")
        self.btn1.clicked.connect(self.client)
        self.btn2 = QPushButton('Администратор', self)
        self.btn2.setFixedSize(300, 100)
        self.btn2.setStyleSheet("background-color: orange;border : 2px solid black;border-radius: 20px;font: bold 30px")
        self.btn2.clicked.connect(self.admin)

        self.lay.addWidget(self.btn1)
        self.lay.addWidget(self.btn2)

        self.setLayout(self.lay)

    def paintEvent(self, e):
        pix = self.pix.scaled(self.size())
        p = QPainter(self)
        p.drawPixmap(0, 0, pix)

    def client(self):
        self.mode_return = 0
        self.switch_window.emit()

    def admin(self):
        # password, ok_pressed = QInputDialog.getText(self, "Введите ключ",
        #                                             "Ваш ключ для администрирования:")
        # if ok_pressed:
        #     if password in special_keys:
        self.mode_return = 1
        self.switch_window.emit()
    #     else:
    #         dlg = QMessageBox(self)
    #         dlg.setWindowTitle('Неверный ключ')
    #         dlg.setText(
    #             f"Ключа нет в списке программы")
    #         dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    #         dlg.setIcon(QMessageBox.Icon.Warning)
    #         button = dlg.exec()


class Client1(QMainWindow):
    switch_window = pyqtSignal()
    back_win = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('res\\UI files\\client_wnd.ui', self)
        self.setWindowTitle('Просмотр актуальных сеансов')
        self.pix = QPixmap("res\\pictures\\backgrounds\\cinema_background_2.jpeg")
        self.setWindowIcon(QIcon('res\\pictures\\icons\\films_icon.png'))

        self.con = sqlite3.connect('proj_db')
        cur = self.con.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Cinemas (id INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT, name TEXT)')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Films (id INTEGER PRIMARY KEY AUTOINCREMENT, durability TEXT, name TEXT)')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Halls (id INTEGER PRIMARY KEY AUTOINCREMENT, size TEXT,'
            ' cinema_id INTEGER REFERENCES Cinemas (id))')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Sessions (id INTEGER PRIMARY KEY ON CONFLICT ROLLBACK '
            'AUTOINCREMENT UNIQUE ON CONFLICT ROLLBACK, time_start TEXT, price INTEGER, '
            'hall_id INTEGER REFERENCES Halls (id), film_id INTEGER REFERENCES Films (id))')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS Posters (id INTEGER PRIMARY KEY AUTOINCREMENT, poster BLOB)')
        cur.execute('CREATE TABLE IF NOT EXISTS Places_mats (id INTEGER PRIMARY KEY AUTOINCREMENT, places_mat TEXT)')
        self.choose_cinema_comboBox.currentTextChanged.connect(self.choose_cinema)
        self.past_btn.setStyleSheet(
            "background-color: gold;border : 2px solid black;border-radius: 5px;font: bold 15px")
        self.past_btn.clicked.connect(self.past)
        self.next_btn.setStyleSheet(
            "background-color: gold;border : 2px solid black;border-radius: 5px;font: bold 15px")
        self.next_btn.clicked.connect(self.next)
        self.reserve_btn.setStyleSheet(
            "background-color: gold;border : 2px solid black;border-radius: 5px;font: bold 15px")
        self.reserve_btn.clicked.connect(self.order)
        self.add_user_btn.setStyleSheet(
            "background-color: gold;border : 2px solid black;border-radius: 5px;font: bold 15px")
        self.add_user_btn.clicked.connect(self.add_user)
        self.check_btn.setStyleSheet(
            "background-color: gold;border : 2px solid black;border-radius: 5px;font: bold 12px")
        self.check_btn.clicked.connect(self.check)
        self.back_btn.setStyleSheet(
            "background-color: gold;border : 2px solid black;border-radius: 5px;font: bold 10px")
        self.back_btn.clicked.connect(self.back)
        cinemas = cur.execute("SELECT id, name FROM Cinemas").fetchall()
        for id, name in cinemas:
            self.choose_cinema_comboBox.insertItem(id, f"{name}")
        self.choose_cinema_comboBox.setStyleSheet('background: purple; color: rgb(255, 215, 215); font: bold 12px')
        self.film_name_ret.setStyleSheet('color: rgb(22, 255, 18); font: italic bold 15px')
        self.price_ret.setStyleSheet('color: rgb(22, 255, 18); font: italic bold 20px')
        self.time_start_ret.setStyleSheet('color: rgb(22, 255, 18); font: italic bold 20px')
        self.film_dur_ret.setStyleSheet('color: rgb(22, 255, 18); font: italic bold 20px')
        self.cinema_lab.setStyleSheet('color: rgb(216, 219, 9); font: italic bold 20px')
        self.poster_lab.setStyleSheet('frame: 10px')

    def paintEvent(self, par):
        pix = self.pix.scaled(self.size())
        p = QPainter(self)
        p.drawPixmap(0, 0, pix)

    def choose_cinema(self):
        cur = self.con.cursor()
        curcinema = self.choose_cinema_comboBox.currentText()
        self.films = cur.execute(
            "SELECT Films.id, durability, Films.name, Posters.poster, price, time_start, places_mat, "
            "Sessions.id FROM Sessions JOIN Films ON Sessions.film_id = Films.id JOIN Halls"
            " ON Sessions.hall_id = Halls.id JOIN Cinemas ON Halls.cinema_id = Cinemas.id JOIN Posters"
            " ON Films.id = Posters.id JOIN Places_mats ON Sessions.id = Places_mats.id WHERE Cinemas.name = ?",
            (curcinema,)).fetchall()
        self.curind = 0
        if self.films:
            if len(self.films[self.curind]) == 8 and self.films[self.curind][3] != 'no_image':
                qpix = QPixmap()
                qpix.loadFromData(bytes(self.films[self.curind][3]))
                qpix = qpix.scaled(620, 360)
                self.poster_lab.setPixmap(qpix)
                self.film_name_ret.setText(f"Название фильма: {self.films[self.curind][2]}")
                self.film_dur_ret.setText(f"Продолжительность: {self.films[self.curind][1]} мин")
                self.price_ret.setText(f"Цена билета: {str(self.films[self.curind][4])} руб")
                self.time_start_ret.setText(f"Начало: {str(self.films[self.curind][5])}")
            elif self.films[self.curind][3] == 'no_image':
                qpix = QPixmap('res\\pictures\\absence pictures\\no_image.jpg')
                qpix = qpix.scaled(620, 360)
                self.poster_lab.setPixmap(qpix)
                self.film_name_ret.setText(f"Название фильма: {self.films[self.curind][2]}")
                self.film_dur_ret.setText(f"Продолжительность: {self.films[self.curind][1]} мин")
                self.price_ret.setText(f"Цена билета: {str(self.films[self.curind][4])} руб")
                self.time_start_ret.setText(f"Начало: {str(self.films[self.curind][5])}")
            self.sessions_flag = True
        else:
            qpix = QPixmap('res\\pictures\\absence pictures\\no_sessions.jpg')
            qpix = qpix.scaled(620, 360)
            self.poster_lab.setPixmap(qpix)
            self.film_name_ret.setText('')
            self.film_dur_ret.setText('')
            self.price_ret.setText(str(0))
            self.time_start_ret.setText('00:00')
            self.sessions_flag = False

    def past(self):
        if self.curind != 0:
            self.curind -= 1
        else:
            self.curind = len(self.films) - 1
        if self.films:
            if self.films[self.curind][3] != 'no_image':
                qpix = QPixmap()
                qpix.loadFromData(bytes(self.films[self.curind][3]))
                qpix = qpix.scaled(620, 360)
                self.poster_lab.setPixmap(qpix)
            elif self.films[self.curind][3] == 'no_image':
                qpix = QPixmap('res\\pictures\\absence pictures\\no_image.jpg')
                qpix = qpix.scaled(620, 360)
                self.poster_lab.setPixmap(qpix)
            self.film_name_ret.setText(f"Название фильма: {self.films[self.curind][2]}")
            self.film_dur_ret.setText(f"Продолжительность: {self.films[self.curind][1]} мин")
            self.price_ret.setText(f"Цена билета: {str(self.films[self.curind][4])} руб")
            self.time_start_ret.setText(f"Начало: {str(self.films[self.curind][5])}")

    def next(self):
        if self.curind != len(self.films) - 1:
            self.curind += 1
        else:
            self.curind = 0
        if self.films:
            if self.films[self.curind][3] != 'no_image':
                qpix = QPixmap()
                qpix.loadFromData(bytes(self.films[self.curind][3]))
                qpix = qpix.scaled(620, 360)
                self.poster_lab.setPixmap(qpix)
            elif self.films[self.curind][3] == 'no_image':
                qpix = QPixmap('res\\pictures\\absence pictures\\no_image.jpg')
                qpix = qpix.scaled(620, 360)
                self.poster_lab.setPixmap(qpix)
            self.film_name_ret.setText(f"Название фильма: {self.films[self.curind][2]}")
            self.film_dur_ret.setText(f"Продолжительность: {self.films[self.curind][1]} мин")
            self.price_ret.setText(f"Цена билета: {str(self.films[self.curind][4])} руб")
            self.time_start_ret.setText(f"Начало: {str(self.films[self.curind][5])}")

    def order(self):
        if self.sessions_flag:
            self.email, ok_pressed_1 = QInputDialog.getText(self, "Введите email",
                                                            "ВАЖНО: Пользователь должен быть зарегистрирован "
                                                            "в базе данных.\nEmail:")
            if ok_pressed_1:
                self.password, ok_pressed_2 = QInputDialog.getText(self, "Введите пароль",
                                                                   "Пароль:")
                if ok_pressed_2:
                    try:
                        self.con = sqlite3.connect('proj_db')
                        cur = self.con.cursor()
                        res = cur.execute("SELECT id, email, password FROM Users WHERE email = ? AND password = ?",
                                          (self.email, self.password)).fetchall()
                        if res[0]:
                            self.switch_window.emit()
                    except Exception:
                        dlg = QMessageBox(self)
                        dlg.setWindowTitle('Неверный логин или пароль')
                        dlg.setText(
                            f"Сначала зарегистрируйтесь в системе (кнопка справа вверху).")
                        dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                        dlg.setIcon(QMessageBox.Icon.Warning)
                        button = dlg.exec()

    def add_user(self):
        self.email, ok_pressed_1 = QInputDialog.getText(self, "Введите email",
                                                        "Введите настоящий email покупателя:")
        if ok_pressed_1:
            if '@' not in self.email:
                self.add_user()
            else:
                self.password = self.add_user2()
                self.con = sqlite3.connect('proj_db')
                cur = self.con.cursor()
                cur.execute("INSERT INTO Users(email, password) VALUES (?, ?)", (self.email, self.password))
                self.con.commit()
                self.con.close()

                dlg = QMessageBox(self)
                dlg.setWindowTitle('Успешно')
                dlg.setText(
                    f"Теперь вы добавлены в базу данных.")
                dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                dlg.setIcon(QMessageBox.Icon.Information)
                button = dlg.exec()

    def add_user2(self):
        password, ok_pressed_2 = QInputDialog.getText(self, "Придумайте пароль",
                                                      "Пароль:")
        if ok_pressed_2:
            if len(password) < 8 or password.isalpha() or password.isdigit():
                return self.add_user3()
            return password

    def add_user3(self):
        password, ok_pressed_2 = QInputDialog.getText(self, "Придумайте пароль",
                                                      "Пароль (должен содержать не менее 8 символов, "
                                                      "хотя бы одну цифру и букву):")
        if ok_pressed_2:
            if len(password) < 8 or password.isalpha() or password.isdigit():
                return self.add_user3()
            return password

    def check(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        try:
            with open(fname, 'r', encoding='UTF-8') as file:
                data = file.read().split('\n')
                sessionid = int(data[-1].split()[-1])
                place = data[-3].split(': ')[-1]
                email = data[-4].split()[-1]
                con = sqlite3.connect('proj_db')
                cur = con.cursor()
                places_mat = cur.execute("SELECT places_mat FROM Places_mats WHERE id = ?", (sessionid,)).fetchall()[0][
                    0]
                flag = False
                places_mat = [val.split(',') for val in places_mat.split()]
                for i in range(len(places_mat)):
                    for j in range(len(places_mat[0])):
                        if places_mat[i][j] == email and len(places_mat) - i == int(place.split()[0]) and j + 1 == int(
                                place.split()[2]):
                            dlg = QMessageBox(self)
                            dlg.setWindowTitle('Проверка чека')
                            dlg.setText(
                                f"Ваш чек действителен")
                            dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                            dlg.setIcon(QMessageBox.Icon.Information)
                            button = dlg.exec()
                            flag = True
                            break
                    if flag:
                        break
                if not flag:
                    raise Exception
        except Exception:
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Проверка чека')
            dlg.setText(
                f"Ваш чек не действителен")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            dlg.setIcon(QMessageBox.Icon.Warning)
            button = dlg.exec()

    def back(self):
        self.back_win.emit()


class Client2(QWidget):
    update_window = pyqtSignal()
    back_win = pyqtSignal()

    def __init__(self, film, email):
        super().__init__()
        self.setWindowTitle('Бронирование мест')
        self.setWindowIcon(QIcon('res\\pictures\\icons\\seats_icon.png'))
        self.pix = QPixmap("res\\pictures\\backgrounds\\cinema_background_3.jpg")
        self.email = email
        self.main_lay = QVBoxLayout(self)
        self.labs_lay = QHBoxLayout(self)
        self.places_lay = QGridLayout(self)
        self.hor1_lay = QHBoxLayout(self)
        self.hor2_lay = QHBoxLayout(self)
        self.hor3_lay = QHBoxLayout(self)
        self.lay_of_places_and_mon_lab = QVBoxLayout(self)
        self.load_widg(film)

    def load_widg(self, film):
        self.film = film
        self.name_lab = QLabel(f'Название: {self.film[2]}', self)
        self.name_lab.setStyleSheet('font: 15px')
        self.price_lab = QLabel(f'Цена: {self.film[4]} руб', self)
        self.price_lab.setStyleSheet('font: 15px')
        self.time_start_lab = QLabel(f'Время начала: {self.film[5]}', self)
        self.time_start_lab.setStyleSheet('font: 15px')
        self.durability_lab = QLabel(f'Продолжительность: {self.film[1]} мин', self)
        self.durability_lab.setStyleSheet('font: 15px')
        self.places_mat = [i.split(',') for i in self.film[6].split()]
        self.x = len(self.places_mat)
        self.y = len(self.places_mat[0])
        self.dict_for_places = {}
        for i in range(self.x):
            for j in range(self.y):
                self.btn = QPushButton(str(self.x - i) + ' ряд ' + str(j + 1) + ' место', self)
                if self.places_mat[i][j] == '0':
                    self.btn.setStyleSheet('background: rgb(26, 194, 23); border-radius : 5;')
                    self.dict_for_places[str(self.x - i) + ' ряд ' + str(j + 1) + ' место'] = (i, j)
                    self.btn.clicked.connect(self.reserve)
                elif self.places_mat[i][j] == self.email:
                    self.btn.setStyleSheet('background: rgb(200,140,25); border-radius : 5;')
                    self.dict_for_places[str(self.x - i) + ' ряд ' + str(j + 1) + ' место'] = (i, j)
                    self.btn.clicked.connect(self.unreserve)
                else:
                    self.btn.setStyleSheet('background: rgb(180,25,30); border-radius : 5;')
                    self.dict_for_places[str(self.x - i) + ' ряд ' + str(j + 1) + ' место'] = (i, j)
                self.places_lay.addWidget(self.btn, i, j)
        for i in range(self.x):
            self.lab = QLabel(f'{str(i + 1)} ряд', self)
            self.places_lay.addWidget(self.lab, self.x - i - 1, self.y + 1)
        self.mon_lab = QLabel('Кликните по месту, которое хотите забронировать. (Экран находится внизу)')
        self.mon_lab.setStyleSheet('font: 20px')
        self.mon_lab1 = QLabel('- свободные места', self)
        self.mon_lab1.setStyleSheet('color: rgb(26, 194, 23); font: bold 15px')
        self.mon_lab2 = QLabel('- места, которые вы забронировали', self)
        self.mon_lab2.setStyleSheet('color: rgb(200,140,25); font: bold 15px')
        self.mon_lab3 = QLabel('- занятые места', self)
        self.mon_lab3.setStyleSheet('color: rgb(180,25,30); font: bold 15px')

        self.mon_btn1 = QPushButton(' ', self)
        self.mon_btn1.setStyleSheet('background: rgb(26, 194, 23); border-radius : 5;')
        self.mon_btn1.setFixedSize(25, 25)
        self.mon_btn2 = QPushButton(' ', self)
        self.mon_btn2.setStyleSheet('background: rgb(200,140,25); border-radius : 5;')
        self.mon_btn2.setFixedSize(25, 25)
        self.mon_btn3 = QPushButton(' ', self)
        self.mon_btn3.setStyleSheet('background: rgb(180,25,30); border-radius : 5;')
        self.mon_btn3.setFixedSize(25, 25)

        self.back_btn = QPushButton('Вернуться к просмотру сеансов', self)
        self.back_btn.setStyleSheet('background: rgb(23, 176, 166); border-radius: 5')
        self.back_btn.clicked.connect(self.back)

        self.labs_lay.addWidget(self.name_lab)
        self.labs_lay.addWidget(self.price_lab)
        self.labs_lay.addWidget(self.time_start_lab)
        self.labs_lay.addWidget(self.durability_lab)

        self.hor1_lay.addWidget(self.mon_btn1)
        self.hor1_lay.addWidget(self.mon_lab1)
        self.hor2_lay.addWidget(self.mon_btn2)
        self.hor2_lay.addWidget(self.mon_lab2)
        self.hor3_lay.addWidget(self.mon_btn3)
        self.hor3_lay.addWidget(self.mon_lab3)

        self.lay_of_places_and_mon_lab.addLayout(self.places_lay)
        self.lay_of_places_and_mon_lab.addWidget(self.mon_lab)
        self.lay_of_places_and_mon_lab.addLayout(self.hor1_lay)
        self.lay_of_places_and_mon_lab.addLayout(self.hor2_lay)
        self.lay_of_places_and_mon_lab.addLayout(self.hor3_lay)

        self.main_lay.addLayout(self.labs_lay)
        self.main_lay.addLayout(self.lay_of_places_and_mon_lab)
        self.main_lay.addWidget(self.back_btn)

    def paintEvent(self, par):
        pix = self.pix.scaled(self.size())
        p = QPainter(self)
        p.drawPixmap(0, 0, pix)

    def reserve(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Занять место.')
        dlg.setText("Вы точно хотите занять это место?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            btn_text = self.sender().text()
            self.line = self.dict_for_places[btn_text][0]
            self.place = self.dict_for_places[btn_text][1]
            check_file_name = f'check{self.film[7]}{self.line}{self.place}.txt'

            with open(check_file_name, 'w', encoding='UTF-8') as f:
                f.write('Чек\n')
                f.write('-' * 20 + '\n')
                f.write(f"Название фильма: {self.film[2]}\n")
                f.write(f"Время начала: {self.film[5]}\n")
                f.write(f"Продолжительность сеанса: {self.film[1]}\n")
                f.write(f"Цена билета: {self.film[4]}\n")
                f.write(f"Email пользователя: {self.email}\n")
                f.write(f"Положение в зале: {btn_text}\n")
                f.write('-' * 20 + '\n')
                f.write(f"Id сеанса: {self.film[7]}")
            self.places_mat[self.line][self.place] = self.email
            places_mat_remade_to_str = ' '.join([','.join(i) for i in self.places_mat])
            con = sqlite3.connect('proj_db')
            cur = con.cursor()
            cur.execute("UPDATE Places_mats SET places_mat = ? WHERE id = ?", (places_mat_remade_to_str, self.film[7]))
            con.commit()
            con.close()
            self.film = (self.film[0], self.film[1], self.film[2], self.film[3], self.film[4], self.film[5],
                         places_mat_remade_to_str, self.film[7])
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Занятие резерва.')
            dlg.setText(f"Теперь вы зарезервированы на это место.\nЧек скачан, название файла: {check_file_name}")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            dlg.setIcon(QMessageBox.Icon.Information)
            button = dlg.exec()
            self.update_win()

    def unreserve(self):
        btn_text = self.sender().text()
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Удаление бронирования.')
        dlg.setText("Вы хотите удалить ваше бронирование этого места? (Ваш чек станет недействительным.)")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            self.line = self.dict_for_places[btn_text][0]
            self.place = self.dict_for_places[btn_text][1]
            self.places_mat[self.line][self.place] = '0'
            places_mat_remade_to_str = ' '.join([','.join(i) for i in self.places_mat])
            con = sqlite3.connect('proj_db')
            cur = con.cursor()
            cur.execute("UPDATE Places_mats SET places_mat = ? WHERE id = ?", (places_mat_remade_to_str, self.film[7]))
            con.commit()
            con.close()
            self.film = (self.film[0], self.film[1], self.film[2], self.film[3], self.film[4], self.film[5],
                         places_mat_remade_to_str, self.film[7])
            self.update_win()

    def update_win(self):
        self.update_window.emit()

    def back(self):
        self.back_win.emit()


class ShowCinemas(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('proj_db')
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
        db.setDatabaseName('proj_db')
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
        db.setDatabaseName('proj_db')
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
        db.setDatabaseName('proj_db')
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
        self.setWindowIcon(QIcon('res\\pictures\\icons\\calendar_icon.png'))
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


class Admin1(QMainWindow):
    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('res\\UI files\\admin_wnd.ui', self)
        self.setWindowTitle('Добавление/удаление значений базы данных')
        self.setWindowIcon(QIcon('res\\pictures\\icons\\redact_icon.png'))
        self.pix = QPixmap("res\\pictures\\backgrounds\\cinema_background_4.jpg")
        self.con = sqlite3.connect('proj_db')
        cur = self.con.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Cinemas (id INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT, name TEXT)')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Films (id INTEGER PRIMARY KEY AUTOINCREMENT, durability TEXT, name TEXT)')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Halls (id INTEGER PRIMARY KEY AUTOINCREMENT, size TEXT,'
            ' cinema_id INTEGER REFERENCES Cinemas (id))')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Sessions (id INTEGER PRIMARY KEY ON CONFLICT ROLLBACK '
            'AUTOINCREMENT UNIQUE ON CONFLICT ROLLBACK, time_start TEXT, price INTEGER, '
            'hall_id INTEGER REFERENCES Halls (id), film_id INTEGER REFERENCES Films (id))')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS Posters (id INTEGER PRIMARY KEY AUTOINCREMENT, poster BLOB)')
        cur.execute('CREATE TABLE IF NOT EXISTS Places_mats (id INTEGER PRIMARY KEY AUTOINCREMENT, places_mat TEXT)')
        self.add_cinema_btn.clicked.connect(self.add_cinema)
        self.add_hall_btn.clicked.connect(self.add_hall)
        self.add_session_btn.clicked.connect(self.add_session)
        self.add_film_btn.clicked.connect(self.add_film)
        self.add_poster_btn.clicked.connect(self.add_poster)
        self.add_time_start_btn.clicked.connect(self.add_time_start)

        self.show_cinemas_window = ShowCinemas()
        self.show_cinemas.triggered.connect(self.show_cinemas_table)
        self.show_halls_window = ShowHalls()
        self.show_halls.triggered.connect(self.show_halls_table)
        self.show_sessions_window = ShowSessions()
        self.show_sessions.triggered.connect(self.show_sessions_table)
        self.show_films_window = ShowFilms()
        self.show_films.triggered.connect(self.show_films_table)

        self.del_cinema_btn.clicked.connect(self.del_cinema)
        self.del_hall_btn.clicked.connect(self.del_hall)
        self.del_session_btn.clicked.connect(self.del_session)
        self.del_film_btn.clicked.connect(self.del_film)

        self.back_btn.clicked.connect(self.back)

    def paintEvent(self, par):
        pix = self.pix.scaled(self.size())
        p = QPainter(self)
        p.drawPixmap(0, 0, pix)

    def add_cinema(self):
        try:
            cur = self.con.cursor()
            film_name = self.enter_cinema_name_for_cinema.text()
            opt_id = self.enter_id_for_cinema_opt.text()
            if film_name and opt_id:
                cur.execute("INSERT INTO Cinemas (id, name) VALUES (?, ?)", (opt_id, film_name))
                self.con.commit()
                self.show_cinemas_window = ShowCinemas()
                self.statusBar().showMessage(f"Кинотеатр {film_name} успешно добавлен")
            elif film_name:
                cur.execute("INSERT INTO Cinemas (name) VALUES (?)", (film_name,))
                self.con.commit()
                self.show_cinemas_window = ShowCinemas()
                self.statusBar().showMessage(f"Кинотеатр {film_name} успешно добавлен")
            else:
                raise Exception
        except Exception:
            self.statusBar().showMessage(f"Данные о кинотеатре введены некорректно")

    def add_hall(self):
        try:
            cur = self.con.cursor()
            cinema_id = self.enter_cinema_id_for_hall.text()
            size = self.enter_hall_size_for_hall.text()
            opt_id = self.enter_id_for_hall_opt.text()
            if cinema_id and size and opt_id:
                if not size.split('*')[0].isdigit() or not size.split('*')[1].isdigit() or len(size.split('*')) != 2:
                    raise Exception
                cur.execute("INSERT INTO Halls (id, cinema_id, size) VALUES (?, ?, ?)", (opt_id, cinema_id, size))
                self.con.commit()
                self.show_halls_window = ShowHalls()
                cin = cur.execute("SELECT name FROM Cinemas WHERE id = ?", (cinema_id,)).fetchall()
                self.statusBar().showMessage(f"Зал для кинотеатра {cin[0][0]} успешно добавлен")
            elif cinema_id and size:
                if not size.split('*')[0].isdigit() or not size.split('*')[1].isdigit() or len(size.split('*')) != 2:
                    raise Exception
                cur.execute("INSERT INTO Halls (cinema_id, size) VALUES (?, ?)", (cinema_id, size))
                self.con.commit()
                self.show_halls_window = ShowHalls()
                cin = cur.execute("SELECT name FROM Cinemas WHERE id = ?", (cinema_id,)).fetchall()
                self.statusBar().showMessage(f"Зал для кинотеатра {cin[0][0]} успешно добавлен")
            else:
                raise Exception
        except Exception:
            self.statusBar().showMessage(f"Данные о зале введены некорректно")

    def add_session(self):
        try:
            cur = self.con.cursor()
            hall_id = self.enter_hall_id_for_session.text()
            price = self.enter_price_for_session.text()
            film_id = self.enter_film_id_for_session.text()
            time_start = self.enter_time_start_for_session.text()
            opt_id = self.enter_id_for_session_opt.text()
            size = cur.execute("SELECT size FROM Halls WHERE id = ?", (hall_id,)).fetchall()[0][0]
            if hall_id and price and film_id and time_start and opt_id:
                if not price.isdigit() or len(time_start.split('-')) != 3 or len(time_start.split()) != 2:
                    raise Exception
                cur.execute(
                    "INSERT INTO Sessions (id, hall_id, price, film_id, time_start) VALUES (?, ?, ?, ?, ?)",
                    (opt_id, hall_id, price, film_id, time_start))
                cur.execute("INSERT INTO Places_mats (id, places_mat) VALUES (?, ?)",
                            (opt_id, ' '.join([','.join(['0' for i in
                                                         range(int(
                                                             size.split('*')[
                                                                 0]))]) for j
                                               in
                                               range(int(
                                                   size.split('*')[1]))])))
                self.con.commit()
                self.show_sessions_window = ShowSessions()
                cin = cur.execute(
                    "SELECT Cinemas.name FROM Cinemas JOIN Halls ON Cinemas.id = Halls.cinema_id WHERE Halls.id = ?",
                    (hall_id,)).fetchall()
                self.statusBar().showMessage(f"Зал для кинотеатра {cin[0][0]} успешно добавлен")
            elif hall_id and price and film_id and time_start:
                if not price.isdigit() or len(time_start.split('-')) != 3 or len(time_start.split()) != 2:
                    raise Exception
                cur.execute(
                    "INSERT INTO Sessions (hall_id, price, film_id, time_start) VALUES (?, ?, ?, ?)",
                    (hall_id, price, film_id, time_start))
                cur.execute("INSERT INTO Places_mats (places_mat) VALUES (?)",
                            (' '.join([','.join(['0' for i in
                                                 range(int(
                                                     size.split('*')[
                                                         0]))]) for j
                                       in
                                       range(int(
                                           size.split('*')[1]))]),))
                self.con.commit()
                self.show_sessions_window = ShowSessions()
                cin = cur.execute(
                    "SELECT Cinemas.name FROM Cinemas JOIN Halls ON Cinemas.id = Halls.cinema_id WHERE Halls.id = ?",
                    (hall_id,)).fetchall()
                self.statusBar().showMessage(f"Сеанс для кинотеатра {cin[0][0]} успешно добавлен")
            else:
                raise Exception
        except Exception:
            self.statusBar().showMessage(f"Данные о сеансе введены некорректно")

    def add_poster(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.enter_poster_for_film.setText(fname)

    def add_film(self):
        cur = self.con.cursor()
        film_name = self.enter_film_name_for_film.text()
        dur = self.enter_dur_for_film.text()
        opt_id = self.enter_id_for_film_opt.text()
        poster = self.enter_poster_for_film.text()
        try:
            if film_name and dur:
                if not dur.isdigit():
                    raise Exception
                if poster and opt_id:
                    with open(poster, 'rb') as f:
                        poster = f.read()
                    cur.execute("INSERT INTO Posters (id, poster) VALUES (?)", (opt_id, poster))
                    self.con.commit()
                    self.show_films_window = ShowFilms()
                elif poster:
                    with open(poster, 'rb') as f:
                        poster = f.read()
                    cur.execute("INSERT INTO Posters (poster) VALUES (?)", (poster,))
                    self.con.commit()
                    self.show_films_window = ShowFilms()
                else:
                    cur.execute("INSERT INTO Posters (poster) VALUES (?)", ('no_image',))
                    self.con.commit()
                    self.show_films_window = ShowFilms()
                if opt_id:
                    cur.execute("INSERT INTO Films (id, durability, name) VALUES (?, ?, ?)",
                                (opt_id, dur, film_name))
                    self.con.commit()
                    self.show_films_window = ShowFilms()
                else:
                    cur.execute("INSERT INTO Films (name, durability) VALUES (?, ?)", (film_name, dur))
                    self.con.commit()
                    self.show_films_window = ShowFilms()
                self.statusBar().showMessage(f"Фильм '{film_name}' успешно добавлен")
            else:
                raise Exception
        except Exception:
            self.statusBar().showMessage(f"Данные о фильме введены некорректно")

    def add_time_start(self):
        self.widg = DateChoose()
        self.widg.show()
        self.widg.upd_window.connect(self.add_time_start2)

    def add_time_start2(self):
        self.enter_time_start_for_session.setText(self.widg.ret)
        self.widg.close()

    def del_cinema(self):
        try:
            cur = self.con.cursor()
            cinema_id = self.enter_cinema_id_for_del.text()
            cur.execute("DELETE FROM Cinemas WHERE id = ?", (cinema_id,))
            self.con.commit()
            self.show_cinemas_window = ShowCinemas()
        except Exception:
            self.statusBar().showMessage(f"Данные введены некорректно")

    def del_hall(self):
        try:
            cur = self.con.cursor()
            hall_id = self.enter_hall_id_for_del.text()
            cur.execute("DELETE FROM Halls WHERE id = ?", (hall_id,))
            self.con.commit()
            self.show_halls_window = ShowHalls()
        except Exception:
            self.statusBar().showMessage(f"Данные введены некорректно")

    def del_session(self):
        try:
            cur = self.con.cursor()
            session_id = self.enter_session_id_for_del.text()
            cur.execute("DELETE FROM Sessions WHERE id = ?", (session_id,))
            cur.execute("DELETE FROM Places_mats WHERE id = ?", (session_id,))
            self.con.commit()
            self.show_sessions_window = ShowSessions()
        except Exception:
            self.statusBar().showMessage(f"Данные введены некорректно")

    def del_film(self):
        try:
            cur = self.con.cursor()
            film_id = self.enter_film_id_for_del.text()
            cur.execute("DELETE FROM Films WHERE id = ?", (film_id,))
            cur.execute("DELETE FROM Posters WHERE id = ?", (film_id,))
            self.con.commit()
            self.show_films_window = ShowFilms()
        except Exception:
            self.statusBar().showMessage(f"Данные введены некорректно")

    def show_cinemas_table(self):
        self.show_cinemas_window.show()

    def show_halls_table(self):
        self.show_halls_window.show()

    def show_sessions_table(self):
        self.show_sessions_window.show()

    def show_films_table(self):
        self.show_films_window.show()

    def back(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        super().__init__()
        pass

    def reg(self):
        self.registration = Registration()
        self.registration.switch_window.connect(self.win2)
        self.registration.show()

    def win2(self):
        if self.registration.mode_return == 0:
            self.registration.close()
            self.cl = Client1()
            self.cl.switch_window.connect(self.win3)
            self.cl.show()
            self.cl.back_win.connect(self.back_from_client)
        elif self.registration.mode_return == 1:
            self.registration.close()
            self.ad = Admin1()
            self.ad.show()
            self.ad.switch_window.connect(self.back_from_admin)

    def win3(self):
        film = self.cl.films[self.cl.curind]
        email = self.cl.email
        self.cl.close()
        self.cl = Client2(film, email)
        self.cl.update_window.connect(self.update_win3)
        self.cl.back_win.connect(self.back_from_client2)
        self.cl.show()

    def update_win3(self):
        film = self.cl.film
        email = self.cl.email
        self.cl.close()
        self.cl = Client2(film, email)
        self.cl.update_window.connect(self.update_win3)
        self.cl.back_win.connect(self.back_from_client2)
        self.cl.show()

    def back_from_admin(self):
        self.ad.close()
        self.reg()

    def back_from_client(self):
        self.cl.close()
        self.reg()

    def back_from_client2(self):
        self.cl.close()
        self.win2()


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.reg()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
