import json
from typing import Mapping, List

from .document import Document
from .fileio import FileIO, BinaryFileIO


class Collection:
    def __init__(self, col_name: str, binary_file: FileIO) -> None:
        self._col_name = col_name
        self._binary_file = binary_file

        # Get the data of existing Database or empty database.
        self._database = self._binary_file.read()
        # print(self._database)
        # Initiate a default Collection

        # Check the Collection is already exists or no
        if self._col_name in self._database.keys():

            # Get the existing Collection
            self._collection: list = self._database[self._col_name]

        else:
            # Create new Collection
            self._database[self._col_name] = []
            self._collection: list = self._database[self._col_name]

    def insert(self, document: Mapping) -> int:
        """
        Inserts a single Document into the Database.

        Document should be JSON Object.

        :param document: Document to insert into database
        :return: None
        """
        # Make sure the document implements the ``Mapping`` interface
        if not isinstance(document, Mapping):
            raise ValueError('Document is not a Dictionary')

        # Create a Document
        _document = Document(document)

        # Numbers of Document
        doc_count: int = 0

        # check Document is already exist or not
        if not self._doc_is_exists(_document.id):

            # Append the document into the Collection
            self._collection.append(_document)

            # Add modified Collection to Database
            self._database[self._col_name] = self._collection

            # print(self._database)
            # Write current state of Database into the Database-file
            self._binary_file.write(self._database)

            return doc_count + 1
        else:
            raise ValueError(f"Document id `{_document.id}` is already exists")

    def insert_all(self, document_list: List[Mapping]) -> int:
        """
        Inserts a single ``Document`` into the ``Database``.

        Document should be a ``List`` of ``JSON Object``.

        :param document_list: List of Documents to insert into Database
        :return: Inserted row(s) count
        """

        # Make sure the document_list implements the ``List`` interface.
        if not isinstance(document_list, List):
            raise ValueError('Document is not a List of Dictionary')

        # Numbers of Document
        doc_count: int = 0

        # Iterate over all Documents of document_list & Insert one by one.
        for document in document_list:

            # insert every single document in Database & increment ``doc_count``.
            doc_count += self.insert(document)

        return doc_count


    # ======================== #
    def _doc_is_exists(self, doc_id: str | int) -> bool:
        # Iterate over all Documents of Collection
        for doc in self._collection:
            if doc["_id_"] == doc_id:
                return True

        return False

    def _get_document_by_id(self, doc_id) -> Document | str:
        for doc in self._collection:
            if doc["_id_"] == doc_id:
                return doc
            else:
                return "none"
