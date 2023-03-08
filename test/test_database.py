from filexdb import FileXdb


# Create an instance of Database
db = FileXdb("test_DB", "test_data/db")
db_2 = FileXdb("NewDb", "test_data/db")

# Create a Collection
student_info = db.collection("student_info")
player_info = db.collection("student_info")

student_info.insert_all([
        {"name": "Addy", "roll": "ME/57/19", "dept": "ME", "cgpa": 9.05},
        {"name": "Roman", "roll": "ECE/80/13", "dept": "ECE", "skill": ["game design"], "spc": ["Blinder"]},
        {"name": "Sam"}])

player_info.insert({"name": "Rana", "sport": "Cricket"})


def test_show_collections():
    assert db.show_collections()
    db_2.show_collections()


def test_show():
    assert db.show()
    db_2.show()

    # prettify json object
    assert db.show().prettify()
    assert db_2.show().prettify()


def test_export():
    db.export("test-db-exp", "test_data/export")
    db_2.export("test-db-2-exp", "test_data/export")


