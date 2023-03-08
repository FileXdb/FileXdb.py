import json
import pickle
import os
import io
from abc import ABC, abstractmethod

__all__ = ("FileIO", "JsonFileIO", "BinaryFileIO", "Export")

from typing import Tuple


def create_file(db_name: str, data_dir: str = None):
    """
    Create a file if it doesn't exist yet.

    :param db_name: Database-file to create.
    :param data_dir: Where the Database-file will be stored.
    """

    # Default Database-file path.
    _db_path = db_name

    if data_dir is not None:
        _db_path = os.path.join(data_dir, db_name)

        # Check if path is already exist or not
        if not os.path.exists(_db_path):

            # Check if we need to create data directories
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

    # Create the file by opening it in "a" mode which creates the file if it
    # does not exist yet but does not modify its contents
    if not os.path.exists(_db_path):
        with open(_db_path, 'a'):
            pass


def pre_process(ext: str, db_name: str, data_dir=None):
    """

    :param ext:
    :param db_name:
    :param data_dir:
    :return:
    """

    # Adding ``FileXdb`` specific file extension to the Database-file.
    _file_name = f"{db_name}.{ext}"

    # Setting default Database-file path.
    _file_full_path = _file_name

    # Checking if Data Directory is on root or not.
    if data_dir is not None:
        # Creating Database-file full path by joining data_dir & db_name.
        _file_full_path = os.path.join(data_dir, _file_name)

    return _file_name, _file_full_path


class FileIO(ABC):
    """
    The abstract base class for all FileIO Classes.

    A FileIO (de)serializes the current state of the database and stores it in
    some place.
    """

    # Using ABCMeta as metaclass allows instantiating only storages that have
    # implemented read and write

    @abstractmethod
    def read(self) -> dict:
        """
        Read the current state of the database from the Database-file.

        Any kind of deserialization should go here.

        Return empty dict if the Database-file is empty.
        """

        raise NotImplementedError('To be overridden!')

    @abstractmethod
    def write(self, data: dict):
        """
        Write the current state of the database to the Database-file.

        Any kind of serialization should go here.

        :param data: The current state of the database.
        """

        raise NotImplementedError('To be overridden!')

    @abstractmethod
    def get_export_path(self) -> str:
        """
        Return Database path

        :return: TDatabase path.
        """

        raise NotImplementedError('To be overridden!')



class BinaryFileIO(FileIO):

    def __init__(self, db_name: str, data_dir=None):
        """
        Create a new instance.

        Also creates the Database-file, if it doesn't exist.

        [Recommended] Don't add any file extension

        :param db_name: Name of Database
        :param data_dir: Where to store the data
        """

        super().__init__()

        self._db_name, self._db_file_path = pre_process("fxdb", db_name, data_dir)

        # Create the Database/File if it doesn't exist
        create_file(self._db_name, data_dir)


    def read(self) -> dict:
        """
        Reads existing Database-file, either it is empty or non-empty.

        If empty returns an empty dict, else returns saved Data.

        :return: Database as a python Dictionary.
        """
        database = None

        with open(self._db_file_path, "rb") as file:

            # Get the file size by moving the cursor to the file end and reading its location.
            file.seek(0, os.SEEK_END)
            size = file.tell()

            # check if size of file is 0
            if size:
                # Bring the cursor to the beginning of Database-file
                file.seek(0)

                try:
                    # Load whole Database form Database-file
                    database = pickle.load(file)

                except io.UnsupportedOperation:
                    # Through an Unsupported Operation Error.
                    raise IOError(f"Cannot read file.\n\t`{self._db_name}` is not a database")

            else:
                # Initiate an empty dict as
                database = {}

        return database

    def write(self, data: dict) -> None:
        """
        Write the current state of entire Database to the Database-file.

        :param data: Dictionary object to write on Database.
        :return: None.
        """
        with open(self._db_file_path, "wb") as file:

            # Move the cursor to the beginning of the file just in case.
            file.seek(0)

            # Serialize the database state using the user-provided arguments
            serialized = pickle.dumps(data)

            # Write the serialized data to the file
            try:
                file.write(serialized)
            except io.UnsupportedOperation:
                raise IOError(f"Cannot write to the file.\n\t`{self._db_name}` is not a database")

            # Ensure the file has been written
            file.flush()
            os.fsync(file.fileno())

            # Remove data that is behind the new cursor if the file has gotten shorter.
            file.truncate()

    def get_export_path(self) -> str:
        return self._db_file_path


class JsonFileIO(FileIO):
    def __init__(self, db_name: str, data_dir=None):

        super().__init__()

        self._db_name, self._db_file_path = pre_process("json", db_name, data_dir)

        # Create the Database/File if it doesn't exist
        create_file(self._db_name, data_dir)

    def read(self) -> dict:
        """
        Reads existing Database-file, either it is empty or non-empty.

        If empty returns an empty dict, else returns saved Data.

        :return: Database as a python Dictionary.
        """
        database = None

        with open(self._db_file_path, "r") as file:

            # Get the file size by moving the cursor to the file end and reading its location.
            file.seek(0, os.SEEK_END)
            size = file.tell()

            # check if size of file is 0
            if size:
                # Bring the cursor to the beginning of Database-file
                file.seek(0)

                try:
                    # Load whole Database form Database-file
                    database = json.load(file)

                except io.UnsupportedOperation:
                    # Through an Unsupported Operation Error.
                    raise IOError(f"Cannot read file.\n\t`{self._db_name}` is not a database")

            else:
                # Initiate an empty dict as
                database = {}

        return database

    def write(self, data: dict):
        """
        Write the current state of entire Database to the Database-file.

        :param data: Dictionary object to write on Database.
        :return: None.
        """
        with open(self._db_file_path, "w") as file:

            # Move the cursor to the beginning of the file just in case.
            file.seek(0)

            # Serialize the database state using the user-provided arguments
            serialized = json.dumps(data, indent=4)

            # Write the serialized data to the file
            try:
                file.write(serialized)
            except io.UnsupportedOperation:
                raise IOError(f"Cannot write to the file.\n\t`{self._db_name}` is not a database")

            # Ensure the file has been written
            file.flush()
            os.fsync(file.fileno())

            # Remove data that is behind the new cursor if the file has gotten shorter.
            file.truncate()

    def get_export_path(self) -> str:
        return self._db_file_path


class Export:
    def __init__(self, _data, _file_name=None, _file_dir=None, _mode="json") -> None:
        """
        Exports data into different readable file.

        :param _file_name: Where to export.
        :param _file_dir: Parent dir.
        :param _data: Data to export.
        :param _mode: Export to which mode.
        """

        # Caching arguments
        self.data = _data
        self.file_name = _file_name
        self.file_dir = _file_dir
        self.mode = _mode

        self._db_name, self._db_file_path = pre_process(self.mode, self.file_name, self.file_dir)

        # Create the Database/File if it doesn't exist
        create_file(self._db_name, self.file_dir)

        # check mode
        if self.mode == "json":
            self.to_json(self.data, self._db_file_path)
        else:
            raise TypeError(f"`{self.mode}` is not a appropriate mode to export")



    def to_json(self, _data, _file_path) -> None:
        """
        Exports data into JSON file.

        :param _data: Data to export.
        :param _file_path: Where to export.
        :return: None
        """
        try:
            with open(_file_path, "w") as f:
                json.dump(_data, fp=f, indent=4)

        except Exception as e:
            print(e)
