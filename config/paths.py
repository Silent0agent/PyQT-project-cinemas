from pathlib import Path
import os
import platform

from config.settings import BASE_DIR


class ProjectPaths:
    def __init__(self):
        self.project_root = BASE_DIR

        self.media = self.project_root / 'media'

        self.static = self.project_root / 'static'

        self.ui_files = self.static / 'ui_files'

        # Изображения
        self.images = self.static / 'img'
        self.icons = self.images / 'icons'
        self.backgrounds = self.images / 'backgrounds'
        self.absence_pictures = self.images / 'absence pictures'
        self.posters = self.media / 'posters'

    def get_ui_file(self, filename):
        return str(self.ui_files / filename)

    def get_icon(self, filename):
        return str(self.icons / filename)

    def get_background(self, filename):
        return str(self.backgrounds / filename)

    def get_absence_picture(self, filename):
        return str(self.absence_pictures / filename)

    def get_poster(self, filename):
        return str(self.posters / filename)




def get_downloads_folder() -> Path:
    """Возвращает путь к папке 'Загрузки' для текущего пользователя"""
    system = platform.system()

    if system == "Windows":
        # Windows: обычно C:\Users\<User>\Downloads
        downloads = Path.home() / "Downloads"
    elif system == "Darwin":
        # macOS: /Users/<User>/Downloads
        downloads = Path.home() / "Downloads"
    else:
        # Linux и другие Unix-системы: ~/Downloads
        downloads = Path.home() / "Downloads"

        # Проверяем XDG_DOWNLOAD_DIR (актуально для современных Linux)
        xdg_download_dir = os.environ.get("XDG_DOWNLOAD_DIR")
        if xdg_download_dir:
            downloads = Path(xdg_download_dir)

    # Создаем папку, если ее нет
    downloads.mkdir(exist_ok=True)

    return downloads
def get_check_in_downloads_path(check_filename):
    downloads_folder = get_downloads_folder()
    check_folder = downloads_folder / check_filename
    return str(check_folder)

# Создаем экземпляр для использования в других модулях
paths = ProjectPaths()
