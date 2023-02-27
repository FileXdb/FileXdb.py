import json
from typing import Mapping, List

from .document import Document
from .fileio import FileIO


#            ^__^
#            (oo)\_______
#            (_)\        )\/\
#                ||----w |
#                ||     ||
#           ~~~~~~~~~~~~~~~~~~~~


class Collection:
    def __init__(self, col_name: str, binary_file: FileIO) -> None:
        self._col_name = col_name
        self._binary_file = binary_file

        # Get the data of existing Database or empty database.
        self._database = self._binary_file.read()

        self._cursor: int = 0

        # Initiate a default Collection.
        # Check the Collection is already exists or no.
        if self._col_name in self._database.keys():

            # Get the existing Collection
            self._collection: list = self._database[self._col_name]

        else:
            # Create new Collection
            self._database[self._col_name] = []
            self._collection: list = self._database[self._col_name]

    def insert(self, document: Mapping) -> str:
        """
        Inserts a single Document into the Database.

        Document should be JSON Object.

        :param document: Document to insert into database
        :return: None
        """
        # Make sure the document implements the ``Mapping`` interface
        if not isinstance(document, Mapping):
            raise ValueError('Document is not a Dictionary')

        # Check if user trying to modify "_id_"
        if "_id_" in document.keys():
            raise KeyError(f"You are not allowed to modify key `_id_`")

        # Create a Document
        _document = Document(document)

        # id of Document
        _doc_id: str = _document.id

        # check Document is already exist or not
        if not self._doc_is_exists(_document.id):

            # Append the document into the Collection
            self._collection.append(_document)

            # Add modified Collection to Database
            self._database[self._col_name] = self._collection

            # print(self._database)
            # Write current state of Database into the Database-file
            self._binary_file.write(self._database)

            return _doc_id
        else:
            raise ValueError(f"Document id `{_document.id}` is already exists")

    def insert_all(self, document_list: List[Mapping]) -> List[str]:
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

        return _doc_id

    """ FIND_ONE 
    def __find_one(self, query: Mapping = None) -> Document | None:
        "
        Finds a single ``Document`` of ``Collection``.

        If ``query`` is None then returns all the ``Documents`` of ``Collection``.

        If ``query`` is not None then returns only the first occurrence.

        :param query: Condition to search Document
        :return: Document
        "
        # Default result
        _result = {}

        # Make sure the query implements the ``Mapping`` interface.
        if not isinstance(query, Mapping | None):
            raise ValueError('Document is not a Dictionary')



        # Check if has ``query`` or not
        if query is None:
            _result = self._collection[self._cursor]
            self._reset_cursor()
        else:
            print(self._cursor)
            _result = self._find_document_by_query(query)
            self._reset_cursor()
            _result = _result[self._cursor]

        return _result
    """

    def find(self, query=None, limit=None) -> List[Document]:
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
        if not isinstance(query, Mapping | None):
            raise ValueError('Document is not a Dictionary')

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

            return _result

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
                if _limit_start >= len(_result):
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



        return _result

    def delete(self, query: Mapping = None) -> List[str]:
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

        self._binary_file.write(self._database)

        return _doc_id

    def update(self, document: Mapping, query: Mapping = None) -> List[str]:
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
            self._binary_file.write(self._database)

        return _doc_id

    def count(self, query: Mapping = None, limit: tuple = None) -> int:
        """
        Return amount of Document found.

        :param query: Condition to search Document.
        :param limit: If there is any limit.
        :return: (int) amount of Document found.
        """
        count = len(self.find(query=query, limit=limit))

        return count

    def _reset_cursor(self) -> None:
        """
        Reset Cursor Pointer to 0th index
        :return: None
        """
        self._cursor = 0

    def _find_document_by_query(self, query: Mapping) -> List:
        """
        Finds a single ``Document`` of ``Collection``.

        Returns None if ``query`` is None of any Document not found.

        :param query: Condition to search Document
        :return: Document
        """
        result = []

        # Make sure the query implements the ``Mapping`` interface.
        if not isinstance(query, Mapping | None):
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

        return result

    # ======================== #
    def _doc_is_exists(self, doc_id: str | int) -> bool:
        # Iterate over all Documents of Collection
        for doc in self._collection:
            if doc["_id_"] == doc_id:
                return True

        return False

    def _find_document_by_id(self, doc_id) -> Document | str:
        for doc in self._collection:
            if doc["_id_"] == doc_id:
                return doc
            else:
                return "none"
