from typing import Mapping
import uuid
import json


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
            self._doc = _id_obj
            for k, v in value.items():
                self._doc[k] = v
            self.id = self._doc["_id_"]

        super().__init__(self._doc)

    def beautify(self) -> str:
        """
        Beautify the ``JSON Object`` with new lines & proper indentation.

        Convert `JSON Object`` into `JSON String`` using ``json.dumps()``.

        :return: JSON String
        """

        # Dumping JSON Object & adding indentation
        self._doc = json.dumps(self._doc, indent=4)

        return self._doc


