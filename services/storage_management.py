from django.core.files import File
from django.core.files.storage import FileSystemStorage
from pathlib import Path

from hacktech.settings import BASE_DIR


class StorageManagement:
    __uploaded_excels_dir = f"{BASE_DIR}/uploaded_excels/"

    def __init__(self) -> None:
        self.file = None
        self.storage = FileSystemStorage()

    def save_file(self, file) -> None:
        """
        Save file
        """
        self.storage.save(f"{self.__uploaded_excels_dir}{file.name}", File(file))
        self.file = file

    def get_name(self) -> str:
        """
        Get file name
        """
        return self.file.name

    def get_storage_path(self) -> str:
        """
        Get storage path
        """
        return self.storage.path(f"{self.__uploaded_excels_dir}{self.get_name()}")

    @classmethod
    def get_file(cls, file_path: str):
        """
        Get file
        """
        return Path(file_path)
