from typing import Mapping
import uuid


def _get_id():
    _id = uuid.uuid1()
    return _id.hex


class Document(dict):
    def __init__(self, value: Mapping) -> None:
        self.id = None

        _id_obj = {
            "_id_": _get_id()
        }

        if "_id_" in value.keys():
            self._doc = value
            self.id = value["_id_"]
        else:
            self._doc = (_id_obj | value)
            self.id = self._doc["_id_"]

        super().__init__(self._doc)
