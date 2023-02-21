from typing import Dict, Type, List

from .collection import Collection


class FileXdb:

    def __init__(self, db_name: str, data_dir: str | None):
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

    def collection(self, col_name: str) -> Collection:
        collection = Collection(self._database, self._db_name, col_name)
        # self.database[col_name] = collection

        return collection

    def show_collections(self):
        pass
