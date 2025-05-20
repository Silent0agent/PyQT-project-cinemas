from .db_connection import db_connection


def create_tables():
    """Создает все таблицы базы данных"""
    with db_connection.connect() as conn:
        cursor = conn.cursor()

        # Создание таблиц
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cinemas (
                id INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT, 
                name TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Films (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                durability TEXT, 
                name TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Halls (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                size TEXT,
                cinema_id INTEGER REFERENCES Cinemas (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sessions (
                id INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT UNIQUE ON CONFLICT ROLLBACK, 
                time_start TEXT, 
                price INTEGER, 
                hall_id INTEGER REFERENCES Halls (id), 
                film_id INTEGER REFERENCES Films (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                email TEXT, 
                password TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Places_mats (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                places_mat TEXT
            )
        ''')

        conn.commit()