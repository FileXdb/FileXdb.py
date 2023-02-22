import json

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

    def insert(self, document: dict) -> None:
        """
        Inserts a single Document into the Database.

        Document should be JSON Object.

        :param document: Document to insert into database
        :return: None
        """

        # Append the document into the Collection
        self._collection.append(document)

        # Add modified Collection to Database
        self._database[self._col_name] = self._collection
        # print(self._database)
        # Write current state of Database into the Database-file
        self._binary_file.write(self._database)


