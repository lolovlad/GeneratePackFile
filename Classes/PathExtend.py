from pathlib import Path
from random import choices
import shutil
from string import ascii_letters, digits
from src.settings import settings
import os


class PathExtend:
    def __init__(self, *args):
        dir_path = Path(Path(__file__).parent).parent
        self.__path: Path = Path(dir_path, settings.static_path, *args)

    @property
    def path(self):
        return self.__path

    def __str__(self):
        return str(self.__path)

    def abs_path(self) -> Path:
        return self.__path

    def str_to_path(self, path_file: str):
        self.__path = Path(path_file)

    @classmethod
    def create_file_name(cls, extension: str,
                         size: int = 10,
                         start_name_file: str = "file") -> str:
        st = ascii_letters + digits
        return f"{start_name_file}_{''.join(choices(st, k=size))}.{extension}"

    @classmethod
    def create_folder_name(cls, size=10) -> str:
        st = ascii_letters + digits
        return f"{''.join(choices(st, k=size))}"

    def delete_dir(self):
        shutil.rmtree(self.__path)

    def delete_file(self):
        os.remove(self.__path)

    def move_file(self, new_path_file):
        shutil.copy2(self.__path, new_path_file.abs_path())

    def name_file(self):
        return self.__path.name

    def path_file(self):
        return self.__path.parent

    def list_file_in_folder(self):
        if self.__path.suffix:
            path_folders = self.__path.parent
        else:
            path_folders = self.__path
        content = os.listdir(path_folders)
        return list(content)

    def delete_files_in_folder(self, extend=None):
        for filename in self.list_file_in_folder():
            if extend is None:
                os.remove(Path(self.__path, str(filename)))
            else:
                if filename.endswith(extend):
                    os.remove(Path(self.__path, str(filename)))

    def read_file(self) -> str:
        with open(self.__path, "r") as file:
            return file.read()
