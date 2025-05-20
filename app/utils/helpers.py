from pathlib import Path
from shutil import copyfile
import sys
from config.paths import paths


def save_poster(film_id: int, source_path: str = None) -> bool:
    """
    Сохраняет постер фильма в media/posters/{film_id}.jpg

    Args:
        film_id: ID фильма в базе данных
        source_path: Путь к исходному файлу изображения

    Returns:
        bool: True если сохранение прошло успешно, False в случае ошибки
    """

    try:
        if not source_path:
            src_path = Path(paths.get_absence_picture('no_image.jpg'))
        else:
            src_path = Path(source_path)
        project_root = Path(__file__).parent.parent.parent
        poster_dir = project_root / "media" / "posters"
        dest_path = poster_dir / f"{film_id}.jpg"

        # Проверяем исходный файл
        if not src_path.is_file():
            print(f"Ошибка: файл {src_path} не найден", file=sys.stderr)
            return False

        # Создаем директорию, если ее нет
        poster_dir.mkdir(parents=True, exist_ok=True)

        # Копируем файл с перезаписью, если существует
        copyfile(src_path, dest_path)
        return True

    except Exception as e:
        print(f"Ошибка при сохранении постера: {e}", file=sys.stderr)
        return False
