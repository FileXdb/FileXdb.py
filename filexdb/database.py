from typing import Dict, Type, List

from .collection import Collection
from .fileio import BinaryFileIO, JsonFileIO
from .document import JsonArray

class FileXdb:

    def __init__(self, db_name: str, data_dir=None, mode="binary"):
        """
        Creates a Databased in ``data_dir`` Directory named ``db_name``.

        If Database is already exists, interacts with that.

        [Recommended]
        Don't add any file extension. ``FileXdb`` will create its own file extension ``fxdb``.

        :param db_name: Name of Database without file extension.
        :param data_dir: Where the Database will be stored.
        """
        self._database = {}
        self._db_name = db_name
        self._data_dir = data_dir

        # Creating an instance of FileIO to Read Write Database-File.
        if mode == "binary":
            self._file_handler = BinaryFileIO(self._db_name, self._data_dir)
        elif mode == "json":
            self._file_handler = JsonFileIO(self._db_name, self._data_dir)

    def collection(self, col_name: str) -> Collection:
        """
        Creates a brand-new Collection if the Collection is not exists.

        If Collection is already exists then it interact with it.

        :param col_name: Collection name to interact with.
        :return: An instance of Collection Baseclass.
        """
        # Initiating collection
        collection = Collection(col_name, self._file_handler)

        return collection

    def show_collections(self) -> JsonArray:
        """
        Shows all collections of database.
        :return: List Collections.
        """
        self._database = self._file_handler.read()

        # Initiating empty result list
        _result = JsonArray(list(self._database.keys()))

        return _result


