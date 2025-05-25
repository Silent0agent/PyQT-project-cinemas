from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6 import uic

from app.database.repository import CinemaRepository, HallRepository, SessionRepository, FilmRepository
from app.ui.widgets import ShowCinemas, ShowHalls, ShowSessions, ShowFilms, DateChoose
from app.utils.helpers import save_poster
from config.paths import paths


class AdminWindow(QMainWindow):
    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Загрузка UI файла
        ui_path = paths.get_ui_file('admin_wnd.ui')
        uic.loadUi(ui_path, self)

        # Настройка окна
        self.setWindowTitle('Добавление/удаление значений базы данных')

        # Установка иконки
        icon_path = paths.get_icon('redact_icon.png')
        self.setWindowIcon(QIcon(icon_path))

        # Установка фона
        bg_path = paths.get_background('cinema_background_4.jpg')
        self.pix = QPixmap(bg_path)
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
            cinema_name = self.enter_cinema_name_for_cinema.text()
            optional_id = self.enter_id_for_cinema_opt.text()
            if cinema_name:
                CinemaRepository.add_cinema(cinema_name, cinema_id=optional_id)
                self.show_cinemas_window = ShowCinemas()
                self.statusBar().showMessage(f"Кинотеатр {cinema_name} успешно добавлен")
            else:
                raise Exception
        except Exception:
            self.statusBar().showMessage(f"Данные о кинотеатре введены некорректно")

    def add_hall(self):
        try:
            cinema_id = self.enter_cinema_id_for_hall.text()
            size = self.enter_hall_size_for_hall.text()
            optional_id = self.enter_id_for_hall_opt.text()
            if cinema_id and size:
                if not size.split('*')[0].isdigit() or not size.split('*')[1].isdigit() or len(size.split('*')) != 2:
                    raise Exception
                else:
                    HallRepository.add_hall(cinema_id, size, hall_id=optional_id)
                    self.show_halls_window = ShowHalls()

                    cinema = CinemaRepository.get_cinema_by_id(cinema_id)

                    self.statusBar().showMessage(f"Зал для кинотеатра {cinema['name']} успешно добавлен")
            else:
                raise Exception
        except Exception:
            self.statusBar().showMessage(f"Данные о зале введены некорректно")

    def add_session(self):
        try:
            hall_id = self.enter_hall_id_for_session.text()
            price = self.enter_price_for_session.text()
            film_id = self.enter_film_id_for_session.text()
            time_start = self.enter_time_start_for_session.text()
            optional_id = self.enter_id_for_session_opt.text()
            hall = HallRepository.get_hall_by_id(hall_id)
            size = hall['size']
            if hall_id and price and film_id and time_start:
                if not price.isdigit() or len(time_start.split('-')) != 3 or len(time_start.split()) != 2:
                    raise Exception
                SessionRepository.add_session(hall_id, price, film_id, time_start, size, session_id=optional_id)
                self.show_sessions_window = ShowSessions()

                cinema = CinemaRepository.get_cinema_by_hall_id(hall_id)
                self.statusBar().showMessage(f"Сеанс для кинотеатра {cinema['name']} успешно добавлен")
            else:
                raise Exception
        except Exception:
            self.statusBar().showMessage(f"Данные о сеансе введены некорректно")

    def add_poster(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        if fname.split('.')[-1] not in ['jpg', 'jpeg', 'jpe', 'jfif']:
            self.statusBar().showMessage('Формат постера должен быть в формате jpeg (jpg)')
            return
        self.enter_poster_for_film.setText(fname)

    def add_film(self):
        film_name = self.enter_film_name_for_film.text()
        durability = self.enter_dur_for_film.text()
        optional_id = self.enter_id_for_film_opt.text()
        poster = self.enter_poster_for_film.text()
        try:
            if film_name and durability:
                if not durability.isdigit():
                    raise Exception
                self.show_films_window = ShowFilms()
                FilmRepository.add_film(film_name, durability, optional_id)
                self.show_films_window = ShowFilms()
                film = FilmRepository.get_film_by_name(film_name)
                save_poster(film['id'], poster)
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
            cinema_id = self.enter_cinema_id_for_del.text()
            CinemaRepository.delete_cinema(cinema_id)
            self.show_cinemas_window = ShowCinemas()
            self.statusBar().showMessage(f"Кинотеатр успешно удалён")
        except Exception:
            self.statusBar().showMessage(f"Данные введены некорректно")

    def del_hall(self):
        try:
            hall_id = self.enter_hall_id_for_del.text()
            HallRepository.delete_hall(hall_id)
            self.show_halls_window = ShowHalls()
            self.statusBar().showMessage(f"Зал успешно удалён")
        except Exception:
            self.statusBar().showMessage(f"Данные введены некорректно")

    def del_session(self):
        try:
            session_id = self.enter_session_id_for_del.text()
            SessionRepository.delete_session(session_id)
            self.show_sessions_window = ShowSessions()
            self.statusBar().showMessage(f"Сеанс успешно удалён")
        except Exception:
            self.statusBar().showMessage(f"Данные введены некорректно")

    def del_film(self):
        try:
            film_id = self.enter_film_id_for_del.text()
            FilmRepository.delete_film(film_id)
            self.show_films_window = ShowFilms()
            self.statusBar().showMessage(f"Фильм успешно удалён")
        except Exception as e:
            print(e)
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
