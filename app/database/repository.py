from pathlib import Path
from typing import List, Dict, Optional

from config.paths import paths
from .db_connection import db_connection
from .queries import GET_SESSIONS
import sqlite3
import hashlib
import os


class CinemaRepository:
    @staticmethod
    def add_cinema(name, cinema_id=None) -> int:
        """Добавляет новый кинотеатр и возвращает его ID"""
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            if cinema_id:
                cursor.execute("INSERT INTO Cinemas (id, name) VALUES (?, ?)", (int(cinema_id), name))
            else:
                cursor.execute('INSERT INTO Cinemas (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all_cinemas() -> List[Dict]:
        """Возвращает список всех кинотеатров"""
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM Cinemas')
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_cinema_by_id(cinema_id) -> Optional[Dict]:
        """Возвращает кинотеатр по ID или None, если не найден"""
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM Cinemas WHERE id = ?', (int(cinema_id),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_cinema_by_hall_id(hall_id) -> Optional[Dict]:
        """Возвращает кинотеатр по ID или None, если не найден"""
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Cinemas.name FROM Cinemas JOIN Halls ON Cinemas.id = Halls.cinema_id WHERE Halls.id = ?",
                (int(hall_id),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def delete_cinema(cinema_id) -> bool:
        """Удаляет кинотеатр по ID, возвращает True если удаление успешно"""
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Cinemas WHERE id = ?', (int(cinema_id),))
            conn.commit()
            return cursor.rowcount > 0


class HallRepository:
    @staticmethod
    def add_hall(cinema_id, size: str, hall_id=None) -> int:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            if hall_id:
                cursor.execute("INSERT INTO Halls (id, cinema_id, size) VALUES (?, ?, ?)",
                               (int(hall_id), int(cinema_id), size))
            else:
                cursor.execute("INSERT INTO Halls (cinema_id, size) VALUES (?, ?)", (int(cinema_id), size))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def delete_hall(hall_id) -> bool:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Halls WHERE id = ?', (int(hall_id),))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def get_hall_by_id(hall_id) -> Optional[Dict]:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Halls WHERE id = ?', (int(hall_id),))
            row = cursor.fetchone()
            return dict(row) if row else None


class SessionRepository:
    @staticmethod
    def add_session(hall_id, price, film_id, time_start, size, session_id=None) -> int:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute(
                    "INSERT INTO Sessions (id, hall_id, price, film_id, time_start) VALUES (?, ?, ?, ?, ?)",
                    (int(session_id), int(hall_id), int(price), int(film_id), time_start))
                cursor.execute("INSERT INTO Places_mats (id, places_mat) VALUES (?, ?)",
                               (session_id, ' '.join([','.join(['0' for i in range(int(size.split('*')[0]))]) for j in
                                                      range(int(size.split('*')[1]))])))
            else:
                cursor.execute(
                    "INSERT INTO Sessions (hall_id, price, film_id, time_start) VALUES (?, ?, ?, ?)",
                    (int(hall_id), int(price), int(film_id), time_start))
                cursor.execute("INSERT INTO Places_mats (places_mat) VALUES (?)",
                               (' '.join([','.join(['0' for i in range(int(size.split('*')[0]))]) for j in
                                          range(int(size.split('*')[1]))]),))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_places(session_id):
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Places_mats WHERE id = ?', (int(session_id),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def delete_session(session_id) -> bool:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Halls WHERE id = ?', (int(session_id),))
            cursor.execute("DELETE FROM Places_mats WHERE id = ?", (int(session_id),))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def update_places(places_mat, session_id):
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Places_mats SET places_mat = ? WHERE id = ?", (places_mat, session_id))
            conn.commit()
            return cursor.rowcount > 0


class FilmRepository:
    @staticmethod
    def add_film(name, durability, film_id=None) -> int:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            if film_id:
                cursor.execute("INSERT INTO Films (id, durability, name) VALUES (?, ?, ?)",
                               (int(film_id), int(durability), name))
            else:
                cursor.execute("INSERT INTO Films (durability, name) VALUES (?, ?)",
                               (int(durability), name))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_film_by_name(film_name) -> Optional[Dict]:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Films WHERE name = ?', (film_name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def delete_film(film_id) -> bool:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Films WHERE id = ?', (int(film_id),))
            conn.commit()
            success = cursor.rowcount > 0
        if success:
            poster_path = Path(paths.get_poster(f"{film_id}.jpg"))
            try:
                if poster_path.exists():
                    poster_path.unlink()
                else:
                    print(f"Файл постера {poster_path} не найден")
            except Exception as e:
                print(f"Ошибка при удалении постера: {e}")
                success = False
        return success

    @staticmethod
    def get_film_by_session_id(session_id) -> Optional[Dict]:
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT Films.id, Films.name FROM Films JOIN Sessions ON Films.id = Sessions.film_id WHERE Sessions.id = ?',
                (session_id,))
            row = cursor.fetchone()
            return dict(row) if row else None


class UserRepository:
    @staticmethod
    def _hash_password(password, salt=None):
        """Хеширование пароля с использованием salt"""
        if salt is None:
            salt = os.urandom(32)  # Генерируем случайную salt
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # Количество итераций
        )
        return salt + key  # Сохраняем salt и хеш вместе

    @staticmethod
    def _verify_password(stored_password, provided_password):
        """Проверка пароля"""
        salt = stored_password[:32]  # Извлекаем salt из сохраненного пароля
        stored_key = stored_password[32:]
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            100000
        )
        return new_key == stored_key

    @staticmethod
    def get_user(email, password):
        """Поиск пользователя с проверкой пароля"""
        with db_connection.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Users WHERE email = ?', (email,))
            row = cursor.fetchone()

            if row and UserRepository._verify_password(row['password'], password):
                return dict(row)
            return None

    @staticmethod
    def get_user_by_email(email):
        with db_connection.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Users WHERE email = ?', (email,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    @staticmethod
    def add_user(email, password):
        """Добавление нового пользователя с хешированием пароля"""
        hashed_password = UserRepository._hash_password(password)

        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (email, password) VALUES (?, ?)",
                (email, hashed_password)
            )
            conn.commit()
            return cursor.lastrowid


class MixedRepository:
    @staticmethod
    def get_films(cinema_name) -> List[Dict]:
        """Возвращает словарь, нужный для обработки сеанса"""
        with db_connection.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_SESSIONS, (cinema_name,))
            return [dict(row) for row in cursor.fetchall()]
