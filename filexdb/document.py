from typing import Mapping, List, Any
import uuid
import json
from .fileio import Export

__all__ = ("Document", "JsonArray")


def _get_id():
    _id = uuid.uuid1()
    return _id.hex


class Document(dict):
    def __init__(self, value: Mapping, gen_id: bool = True) -> None:
        self.id = None

        _id_obj = {
            "_id_": _get_id()
        }

        if "_id_" in value.keys():
            self._doc = value
            self.id = value["_id_"]
        elif "_id_" not in value.keys() and not gen_id:
            self._doc = value
        else:
            self._doc = _id_obj
            for k, v in value.items():
                self._doc[k] = v
            self.id = self._doc["_id_"]

        super().__init__(self._doc)

    def prettify(self) -> str:
        """
        Beautify the ``JSON Object`` with new lines & proper indentation.

        Convert `JSON Object`` into `JSON String`` using ``json.dumps()``.

        :return: JSON Object
        """

        # Dumping JSON Object & adding indentation
        _doc: str = json.dumps(self._doc, indent=4)

        return _doc



class JsonArray(list):
    def __init__(self, _value: list) -> None:
        self.value = _value
        super().__init__(self.value)


    def prettify(self) -> str:
        """
        Beautify the ``JSON Array`` with new lines & proper indentation.

        Convert `JSON Array`` into `JSON Array`` using ``json.dumps()``.

        :return: JSON Array
        """

        # Dumping JSON Object & adding indentation
        value: str = json.dumps(self.value, indent=4)

        return value

    def count_item(self) -> int:
        """
        Return amount of Document found.

        :return: (int) amount of Document found.
        """
        count = len(self.value)

        return count

    def export(self, _file_name, _file_dir=None, _mode="json"):
        """

        :param _file_name:
        :param _file_dir:
        :param _mode:
        :return:
        """

        e = Export(self.value, _file_name, _file_dir, _mode)









