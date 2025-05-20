from pathlib import Path

ADMINISTRATION_KEYS = ['gas']
# Корень проекта (определяется относительно расположения settings.py)
BASE_DIR = Path(__file__).parent.parent

# Пути к базе данных
DATABASE_NAME = "cinemas.db"
DATABASE_PATH = BASE_DIR / "app" / "database" / DATABASE_NAME