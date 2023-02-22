import json
import pickle
import os
import io
from abc import ABC, abstractmethod

__all__ = ("FileIO", "JsonFileIO", "BinaryFileIO")


def create_db(db_name: str, data_dir: str = None):
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
    with open(_db_path, 'ab'):
        pass


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


class BinaryFileIO(FileIO):
    def __init__(self, db_name: str, data_dir: str = None):
        """
        Create a new instance.

        Also creates the Database-file, if it doesn't exist.

        [Recommended] Don't add any file extension

        :param db_name: Name of Database
        :param data_dir: Where to store the data
        """

        super().__init__()

        self._data_dir = data_dir

        # Adding ``FileXdb`` specific file extention to the Database-file.
        self._db_name = f"{db_name}.fxdb"

        # Setting default Database-file path.
        self._db_file_path = self._db_name

        # Checking if Data Directory is on root or not.
        if self._data_dir is not None:

            # Creating Database-file full path by joining data_dir & db_name.
            self._db_file_path = os.path.join(self._data_dir, self._db_name)

        # Create the Database/File if it doesn't exist
        create_db(self._db_name, self._data_dir)

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
                # Returns an empty dict as
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


class JsonFileIO(FileIO):
    def __init__(self, db_name):
        super().__init__()
        self.db_name = db_name

    def read(self) -> dict:
        pass

    def write(self, data: dict):
        pass
