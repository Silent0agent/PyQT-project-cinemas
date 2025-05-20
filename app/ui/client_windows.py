from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QFileDialog, \
    QLabel, QGridLayout, QInputDialog, QVBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6 import uic
from app.database.repository import CinemaRepository, MixedRepository, FilmRepository, UserRepository, SessionRepository
from config.paths import paths, get_check_in_downloads_path


class ClientViewSessionsWindow(QMainWindow):
    switch_window = pyqtSignal()
    back_win = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(paths.get_ui_file('client_wnd.ui'), self)
        self.setWindowTitle('Просмотр актуальных сеансов')
        self.curind = 0
        self.sessions = []
        self.pix = QPixmap(paths.get_background('cinema_background_2.jpeg'))
        self.setWindowIcon(QIcon(paths.get_icon('films_icon.png')))
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
        self.add_user_btn.clicked.connect(self.add_user_stage_1)
        self.check_btn.setStyleSheet(
            "background-color: gold;border : 2px solid black;border-radius: 5px;font: bold 12px")
        self.check_btn.clicked.connect(self.check_receipt)
        self.back_btn.setStyleSheet(
            "background-color: gold;border : 2px solid black;border-radius: 5px;font: bold 10px")
        self.back_btn.clicked.connect(self.back)
        cinemas = CinemaRepository.get_all_cinemas()
        for cinema in cinemas:
            self.choose_cinema_comboBox.insertItem(cinema['id'], f"{cinema['name']}")
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
        curcinema = self.choose_cinema_comboBox.currentText()
        current_sessions = self.sessions
        self.sessions = MixedRepository.get_films(curcinema)
        if [session['id'] for session in current_sessions] != [session['id'] for session in self.sessions]:
            self.curind = 0
        if self.sessions:
            current_session = self.sessions[self.curind]
            self.session = current_session
            film = FilmRepository.get_film_by_session_id(current_session['id'])
            qpix = QPixmap()
            with open(paths.get_poster(f"{film['id']}.jpg"), 'rb') as file:
                qpix.loadFromData(file.read())
            qpix = qpix.scaled(620, 360)
            self.poster_lab.setPixmap(qpix)
            self.film_name_ret.setText(f"Название фильма: {current_session['name']}")
            self.film_dur_ret.setText(f"Продолжительность: {current_session['durability']} мин")
            self.price_ret.setText(f"Цена билета: {current_session['price']} руб")
            self.time_start_ret.setText(f"Начало: {current_session['time_start']}")
            self.sessions_flag = True
        else:
            qpix = QPixmap(paths.get_absence_picture('no_sessions.jpg'))
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
            self.curind = len(self.sessions) - 1
        self.choose_cinema()

    def next(self):
        if self.curind != len(self.sessions) - 1:
            self.curind += 1
        else:
            self.curind = 0
        self.choose_cinema()

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
                        user = UserRepository.get_user(self.email, self.password)
                        if user:
                            self.switch_window.emit()
                        else:
                            raise Exception
                    except Exception:
                        dlg = QMessageBox(self)
                        dlg.setWindowTitle('Неверный логин или пароль')
                        dlg.setText(
                            f"Сначала зарегистрируйтесь в системе (кнопка справа вверху).")
                        dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                        cancel_button = dlg.button(QMessageBox.StandardButton.Cancel)
                        cancel_button.setText("Назад")
                        dlg.setIcon(QMessageBox.Icon.Warning)
                        button = dlg.exec()

    def add_user_stage_1(self):
        self.email, ok_pressed_1 = QInputDialog.getText(self, "Введите email",
                                                        "Введите настоящий email покупателя, "
                                                        "который не зарегистрирован в базе данных:")
        if ok_pressed_1:
            if ('@' not in self.email) or UserRepository.get_user_by_email(self.email):
                self.add_user_stage_1()
            else:
                self.password = self.add_user_stage_2()
                UserRepository.add_user(self.email, self.password)
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Успешно')
                dlg.setText(
                    f"Теперь вы добавлены в базу данных.")
                dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                cancel_button = dlg.button(QMessageBox.StandardButton.Cancel)
                cancel_button.setText("Назад")
                dlg.setIcon(QMessageBox.Icon.Information)
                button = dlg.exec()

    def add_user_stage_2(self):
        password, ok_pressed_2 = QInputDialog.getText(self, "Придумайте пароль",
                                                      "Пароль:")
        if ok_pressed_2:
            if len(password) < 8 or password.isalpha() or password.isdigit():
                return self.add_user_stage_3()
            return password

    def add_user_stage_3(self):
        password, ok_pressed_2 = QInputDialog.getText(self, "Придумайте пароль",
                                                      "Пароль (должен содержать не менее 8 символов, "
                                                      "хотя бы одну цифру и букву):")
        if ok_pressed_2:
            if len(password) < 8 or password.isalpha() or password.isdigit():
                return self.add_user_stage_3()
            return password

    def check_receipt(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        try:
            with open(fname, 'r', encoding='UTF-8') as file:
                data = file.read().split('\n')
                session_id = int(data[-1].split()[-1])
                place = data[-3].split(': ')[-1]
                email = data[-4].split()[-1]
                places_mat = SessionRepository.get_places(session_id)['places_mat']
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
                            cancel_button = dlg.button(QMessageBox.StandardButton.Cancel)
                            cancel_button.setText("Назад")
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
            cancel_button = dlg.button(QMessageBox.StandardButton.Cancel)
            cancel_button.setText("Назад")
            dlg.setIcon(QMessageBox.Icon.Warning)
            button = dlg.exec()

    def back(self):
        self.back_win.emit()


class ClientReserveWindow(QWidget):
    update_window = pyqtSignal()
    back_win = pyqtSignal()

    def __init__(self, session, email):
        super().__init__()
        self.setWindowTitle('Бронирование мест')
        self.setWindowIcon(QIcon(paths.get_icon('seats_icon.png')))
        self.pix = QPixmap(paths.get_background('cinema_background_3.jpg'))
        self.email = email
        self.main_lay = QVBoxLayout(self)
        self.labs_lay = QHBoxLayout(self)
        self.places_lay = QGridLayout(self)
        self.hor1_lay = QHBoxLayout(self)
        self.hor2_lay = QHBoxLayout(self)
        self.hor3_lay = QHBoxLayout(self)
        self.lay_of_places_and_mon_lab = QVBoxLayout(self)
        self.load_widg(session)

    def load_widg(self, session):
        self.session = session
        self.name_lab = QLabel(f'Название: {self.session["name"]}', self)
        self.name_lab.setStyleSheet('font: 15px')
        self.price_lab = QLabel(f'Цена: {self.session["price"]} руб', self)
        self.price_lab.setStyleSheet('font: 15px')
        self.time_start_lab = QLabel(f'Время начала: {self.session["time_start"]}', self)
        self.time_start_lab.setStyleSheet('font: 15px')
        self.durability_lab = QLabel(f'Продолжительность: {self.session["durability"]} мин', self)
        self.durability_lab.setStyleSheet('font: 15px')
        self.places_mat = [i.split(',') for i in self.session["places_mat"].split()]
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
                    self.btn.clicked.connect(self.delete_reserve)
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
        yes_button = dlg.button(QMessageBox.StandardButton.Yes)
        yes_button.setText("Да")
        no_button = dlg.button(QMessageBox.StandardButton.No)
        no_button.setText("Нет")
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            btn_text = self.sender().text()
            self.line = self.dict_for_places[btn_text][0]
            self.place = self.dict_for_places[btn_text][1]
            check_file_name = f'check{self.session["id"]}{self.line}{self.place}.txt'

            with open(get_check_in_downloads_path(check_file_name), 'w', encoding='UTF-8') as f:
                f.write('Чек\n')
                f.write('-' * 20 + '\n')
                f.write(f"Название фильма: {self.session['name']}\n")
                f.write(f"Время начала: {self.session['time_start']}\n")
                f.write(f"Продолжительность сеанса: {self.session['durability']}\n")
                f.write(f"Цена билета: {self.session['price']}\n")
                f.write(f"Email пользователя: {self.email}\n")
                f.write(f"Положение в зале: {btn_text}\n")
                f.write('-' * 20 + '\n')
                f.write(f"Id сеанса: {self.session['id']}")
            self.places_mat[self.line][self.place] = self.email
            places_mat_remade_to_str = ' '.join([','.join(i) for i in self.places_mat])
            SessionRepository.update_places(places_mat_remade_to_str, self.session['id'])
            self.session['places_mat'] = places_mat_remade_to_str
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Занятие места.')
            dlg.setText(f"Теперь вы зарезервировали это место.\nЧек скачан, название файла: {check_file_name}")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            cancel_button = dlg.button(QMessageBox.StandardButton.Cancel)
            cancel_button.setText("Назад")
            dlg.setIcon(QMessageBox.Icon.Information)
            button = dlg.exec()
            self.update_win()

    def delete_reserve(self):
        btn_text = self.sender().text()
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Удаление бронирования.')
        dlg.setText("Вы хотите удалить ваше бронирование этого места? (Ваш чек станет недействительным.)")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        yes_button = dlg.button(QMessageBox.StandardButton.Yes)
        yes_button.setText("Да")
        no_button = dlg.button(QMessageBox.StandardButton.No)
        no_button.setText("Нет")
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            self.line = self.dict_for_places[btn_text][0]
            self.place = self.dict_for_places[btn_text][1]
            self.places_mat[self.line][self.place] = '0'
            places_mat_remade_to_str = ' '.join([','.join(i) for i in self.places_mat])
            SessionRepository.update_places(places_mat_remade_to_str, self.session['id'])
            self.session['places_mat'] = places_mat_remade_to_str

            self.update_win()

    def update_win(self):
        self.update_window.emit()

    def back(self):
        self.back_win.emit()
