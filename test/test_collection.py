from filexdb import FileXdb


db = FileXdb("testDb", 'data')

data = {"name": "India", "capital": "New Delhi", "city": ["Kolkata", "Bangalore", "Mumbai", "Delhi"]}
data_list = [
    {"name": "Nepal", "capital": "Kathmandu", "city": []},
    {"name": "Russia", "capital": "Moscow"}
]

countries = db.collection("countries")
countries.insert(data)
countries.insert_all(data_list)

