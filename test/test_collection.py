from filexdb import FileXdb


# Create an instance of Database
db = FileXdb("testDb", "data/db")

# Create a Collection
student_info = db.collection("student_info")


def insert_single_document():
    assert student_info.insert({"name": "Sam", "roll": "CSE/17/19", "dept": "CSE"})
    assert student_info.insert({"name": "Bob", "roll": "EE/01/18", "dept": "EE", "skill": ["python", "c++"]})
    assert student_info.insert({"name": "Rana", "dept": "CSE"})


def insert_multiple_document():
    assert student_info.insert_all([
        {"name": "Addy", "roll": "ME/57/19", "dept": "ME", "cgpa": 9.05},
        {"name": "Roman", "roll": "ECE/80/13", "dept": "ECE", "skill": ["game design"], "spc": ["Blinder"]},
        {"name": "Sam"}
    ]
    )


def find_document_1():
    _query_1 = {"name": "Sam"}

    assert student_info.find()                                  # Returns all Documents.
    assert student_info.find(query=_query_1)                    # Returns all Documents matches the ``_query``.
    assert student_info.find(query=_query_1, limit=(1, 3))      # Returns doc[1] to doc[2] matches the ``_query``.
    assert student_info.find(limit=(1, 10))                     # Returns doc[1] to doc[9] of all Documents.


def find_document_2():
    _query_2 = {"name": "Sam", "roll": "CSE/17/19"}

    assert student_info.find()                                  # Returns all Documents.
    assert student_info.find(query=_query_2)                    # Returns all Documents matches the ``_query``.
    assert student_info.find(query=_query_2, limit=(1, 3))      # Returns doc[1] to doc[2] matches the ``_query``.
    assert student_info.find(limit=(1, 10))                     # Returns doc[1] to doc[9] of all Documents.


def delete_document():
    assert student_info.delete({"name": "Addy"})
    assert student_info.delete({"name": "Sam", "roll": "CSE/17/19"})
    assert student_info.delete({"name": "Roman", "roll": "ECE/80/13", "dept": "ECE"})


def update_document():
    assert student_info.update({"passed": True, "mobile": 123456789}, {"name": "Bob"})
    assert student_info.update({"name": "The Sam", "skill": ["C++", "Python"]}, {"name": "Sam"})
    assert student_info.update({"dept": "Computer Science & Engineering"}, {"dept": "CSE"})
