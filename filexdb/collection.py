import json
from typing import Mapping, List

from .document import Document, JsonArray
from .fileio import FileIO


#            ^__^
#            (oo)\_______
#            (_)\        )\/\
#                ||----w |
#                ||     ||
#           ~~~~~~~~~~~~~~~~~~~~


class Collection:
    def __init__(self, col_name: str, file_handler: FileIO) -> None:
        self._col_name = col_name
        self._file_handler = file_handler

        # Get the data of existing Database or empty database.
        self._database = self._get_database()

        # Initiating Collecting
        self._collection = self._get_collection()

        # Cursor
        self._cursor: int = 0



    def insert(self, document: Mapping) -> str:
        """
        Inserts a single Document into the Database.

        Document should be JSON Object.

        :param document: Document to insert into the database.
        :return: Document ID.
        """

        # Make sure the document implements the ``Mapping`` interface
        if not isinstance(document, Mapping):
            raise ValueError('Document is not a Dictionary')

        # Check if user trying to modify "_id_"
        if "_id_" in document.keys():
            raise KeyError(f"You are not allowed to modify key `_id_`")


        # getting Database
        _database = self._get_database()

        # Create a Document
        _document = Document(document)

        # ID of Document
        _doc_id: str = _document.id

        # check Document is already exist or not
        if not self._doc_is_exists(_document.id):

            # Append the document into the Collection
            self._collection.append(_document)

            # Add modified Collection to Database
            _database[self._col_name] = self._collection

            # print(self._database)
            # Write current state of Database into the Database-file
            self._file_handler.write(_database)

            return _doc_id
        else:
            raise ValueError(f"Document id `{_document.id}` is already exists")

    def insert_all(self, document_list: List[Mapping]) -> JsonArray[str]:
        """
        Inserts a single ``Document`` into the ``Database``.

        Document should be a ``List`` of ``JSON Object``.

        :param document_list: List of Documents to insert into Database
        :return: Inserted row(s) count
        """

        # Make sure the document_list implements the ``List`` interface.
        if not isinstance(document_list, List):
            raise ValueError('Document is not a List of Dictionary')

        # id of Document
        _doc_id: List[str] = []

        # Iterate over all Documents of document_list & Insert one by one.
        for document in document_list:
            # insert every single document in Database & increment ``doc_count``.
            _doc_id.append(self.insert(document))

        return JsonArray(_doc_id)

    def find(self, query=None, limit=None) -> JsonArray[Document]:
        """
        Finds all ``Document`` of ``Collection``.

        If ``query`` is None then returns all the ``Documents`` of ``Collection``.

        If ``query`` is not None then find returns all the occurrences.

        :param limit: Amount of Document to fetch
        :param query: Condition to search Document
        :return: List of Document
        """

        # Default result
        _result = []

        # Make sure the query implements the ``Mapping`` interface.
        if query:
            if not isinstance(query, Mapping):
                raise ValueError('Document is not a Dictionary')

        # Make sure the query implements the ``Tuple`` interface.
        if limit:
            if not isinstance(limit, tuple):
                raise ValueError('Document is not a Tuple')

        # if limit, Check everything ok
        _limit_start = _limit_end = None

        if limit and type(limit) == type((1, 3)):
            if len(limit) == 2:

                _limit_start = limit[0]
                _limit_end = limit[1]

                # check if lower limit greater than upper limit
                if _limit_start > _limit_end:
                    raise ValueError("limit[0] must be less than limit[1].")
            else:
                raise ValueError(f"limit is a tuple of 2 values, {len(limit)} is given.")

        # Check if ``query`` is None or not None.
        if query is None:
            # Check if it has a limit or not. If it has a limit do limit specific tasks.
            # Else return the whole Collection.
            if limit is not None:

                # check if lower limit is valid or not
                if _limit_start >= len(self._collection):
                    raise ValueError(
                        f"Lower limit should be smaller than Collection length.\n It must be less than `{len(self._collection)}`. `{_limit_start}` is given.")
                else:
                    _result = self._collection[_limit_start: _limit_end]
            else:
                _result = self._collection

            return JsonArray(_result)

        elif query is not None and type(query) == type({}):
            if limit:
                for i in self._collection:
                    _doc = self._find_document_by_query(query)

                    # Append Document to the result if found
                    if _doc:
                        _result += _doc

                        # Check the result reached to the limit or not
                        if len(_result) >= _limit_end:
                            break

                # Reset the cursor
                self._reset_cursor()

                # check if lower limit is valid or not
                if _limit_start >= len(_result) and _limit_start != 0:
                    raise ValueError(f"lower limit should be smaller than length of result")
                else:
                    # Travers limited result
                    _result = _result[_limit_start: _limit_end]

            else:
                for i in self._collection:
                    _doc = self._find_document_by_query(query)

                    if _doc:
                        _result += _doc
                    else:
                        _result = _result

                self._reset_cursor()

        return JsonArray(_result)

    def delete(self, query=None) -> JsonArray[str]:
        """
        Delete single or multiple Document when meet the Conditions or ``query``.

        [Recommended]
        Use unique identifier as ``query``.

        :param query: Condition to search Document
        :return: int - amount of effected Document
        """
        # IDs of Effected Documents
        _doc_id: List[str] = []

        # Fetching a Documents meet the query
        _documents = self.find(query, None)

        # Fetch every Document & remove from Collection
        for _doc in _documents:
            self._collection.remove(_doc)
            _doc_id.append(_doc["_id_"])

        self._file_handler.write(self._database)

        return JsonArray(_doc_id)

    def update(self, document: Mapping, query=None) -> JsonArray[str]:
        """
        Fetch all the Documents mathc the conditions and update them.

        [Recommended]
        Use a unique identifier as ``query``.

        :param document: New key values to update
        :param query: Condition to search Document.
        :return: List of document ID.
        """
        _documents = self.find(query)
        _new_doc = document

        # IDs of Effected Documents
        _doc_id: List[str] = []

        # Fetch all Documents to update if got multiple.
        for _doc in _documents:
            for key, value in _new_doc.items():

                # Check if user trying to modify "_id_"
                if key == "_id_":
                    raise KeyError(f"You are not allowed to modify key `{key}`")

                # Update Document
                # Create new field if needed.
                _doc[key] = value

            _doc_id.append(_doc["_id_"])

            # Write current state of Database
            self._file_handler.write(self._database)

        return JsonArray(_doc_id)

    def rename(self, new_name: str) -> int:
        """
        This method used to change the name of collection.
        Takes current name & new name to change name of the collection.

        :param new_name: New name for collection.
        :return: Amount of affected collection.
        """

        # Initiating counter
        count = 0

        # Checking the collection is already exist or not
        if new_name not in self._database.keys():

            # Creating new collection and
            # Putting old data into new collection
            self._database[new_name] = self._collection

            # Writing Current database status into the file
            self._file_handler.write(self._database)

            # Remove old collection
            self.drop()

            # Increasing counter
            count += 1

        return count

    def drop(self) -> int:
        """
        Deletes the selected collection from the database

        :return: Amount of affected collection
        """

        # Initiating counter
        count = 0

        # Getting database
        _database = self._file_handler.read()

        # Check database has the collection or not
        if self._col_name in _database.keys():
            # Removing collection from database
            _database.pop(self._col_name)

            # Writing current status of database into the file system.
            self._file_handler.write(_database)

            # Increasing counter
            count += 1

        return count


    # ----------------------------------------------------------------#
    def _get_database(self) -> Document:
        """
        Getting Database

        :return: Database
        """
        # Get the data of existing Database or empty database.
        database = Document(self._file_handler.read(), False)

        return database

    def _get_collection(self) -> JsonArray:
        """
        Getting Collection

        :return: Collection
        """
        # Initiate a default Collection.
        # Check the Collection is already exists or no.
        if self._col_name in self._database.keys():

            # Get the existing Collection
            _collection: JsonArray = self._database[self._col_name]

        else:
            # Create new Collection
            self._database[self._col_name] = JsonArray([])
            _collection: JsonArray = self._database[self._col_name]

        return _collection


    def _reset_cursor(self) -> None:
        """
        Reset Cursor Pointer to 0th index
        :return: None
        """
        self._cursor = 0

    def _find_document_by_query(self, query: Mapping) -> JsonArray[Document]:
        """
        Finds a single ``Document`` of ``Collection``.

        Returns None if ``query`` is None of any Document not found.

        :param query: Condition to search Document
        :return: Document
        """
        result = []

        # Make sure the query implements the ``Mapping`` interface.
        if not isinstance(query, Mapping):
            raise ValueError('Document is not a Dictionary')

        # Get the length on Collection
        _collection_length = len(self._collection)

        # Iterate all the Documents of Collection
        for doc_index in range(self._cursor, _collection_length):

            # Update ``self._doc_index`` with ``doc_index``, to iterate next Document.
            self._cursor = doc_index + 1

            # Get the length on ``query`` to iterate all attributes
            _query_length = len(query)

            # Typecast ``query`` in to a ``list`` to iterate it.
            _query_list = list(query.items())

            # ``_bag_of_query`` indicates the Document is desired or not.
            _bag_of_query = [0] * _query_length

            for i in range(_query_length):

                # Check the ``key`` is belongs to the Documents or not.
                if _query_list[i][0] in self._collection[doc_index]:

                    # Check the ``value`` of ``query`` is same to the Document's or not.
                    if self._collection[doc_index][_query_list[i][0]] == _query_list[i][1]:

                        # If both values are same, then update ``_bag_of_query[i]`` as 1.
                        _bag_of_query[i] = 1

                    else:
                        continue
                else:
                    continue
                    # Check if ``_bag_of_query`` contains any `0` or not.
                    # If it has any value then this is the desired Document.
                    # Else such Document in Collection.

            if 0 not in _bag_of_query:

                # return the Document
                result.append(self._collection[doc_index])

            elif doc_index <= _collection_length:
                # self._doc_index = doc_index
                continue

            else:
                return None

        return JsonArray(result)

    def _doc_is_exists(self, doc_id: str) -> bool:
        # Iterate over all Documents of Collection
        for doc in self._collection:
            if doc["_id_"] == doc_id:
                return True

        return False


