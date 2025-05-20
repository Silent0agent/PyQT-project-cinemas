import sys

from PyQt6.QtWidgets import QApplication
from app.controlers.main_controller import Controller
from app.database.db_connection import db_connection
from app.database.models import create_tables


def main():
    # Инициализация базы данных
    try:
        create_tables()  # Создаем таблицы при старте приложения
        print("Таблицы базы данных успешно созданы/проверены")
    except Exception as e:
        print(f"Ошибка при создании таблиц базы данных: {e}")
        return  # Завершаем приложение при ошибке инициализации БД

    # Создаем и запускаем приложение
    app = QApplication(sys.argv)

    try:
        controller = Controller()
        controller.main_window()  # Инициализация контроллера
    except Exception as e:
        print(f"Ошибка при инициализации контроллера: {e}")
        return

    # Запускаем главный цикл приложения
    exit_code = app.exec()

    # Закрываем соединение с БД при завершении
    db_connection.close()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
