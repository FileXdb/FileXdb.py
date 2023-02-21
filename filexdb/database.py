from typing import Dict, Type, List

from .collection import Collection


class FileXdb:

    def __init__(self, db_name):
        self.database = {}
        self.db_name = db_name

    def collection(self, col_name) -> Collection:
        collection = Collection(self.database, self.db_name, col_name)
        # self.database[col_name] = collection

        return collection

    def show_collections(self):
        pass
