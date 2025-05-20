import sqlite3
from typing import Optional

from config.settings import DATABASE_PATH


class DatabaseConnection:
    def __init__(self, db_name: str = str(DATABASE_PATH)):
        self.db_name = db_name
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Устанавливает соединение с базой данных"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row  # Для доступа к полям по имени
        return self.connection

    def close(self) -> None:
        """Закрывает соединение с базой данных"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None


# Создаем экземпляр для использования в других модулях
db_connection = DatabaseConnection()