from .document import Document
import json


class Collection:
    def __init__(self, database, db_name, col_name: str) -> None:
        self._database = database
        self._db_name = db_name
        self._col_name = col_name

        self._database[self._col_name] = []
        # self._collection = list(self._database[self._col_name])

    def insert(self, doc: dict) -> None:
        _doc = doc
        print(_doc)
        print(self._database)
        # data = list(self._collection).append(doc)
        data = self._database[self._col_name].append(_doc)
        print(self._database)
        with open(f"{self._db_name}.json", "w") as f:
            json.dump(self._database, f, indent=4)

