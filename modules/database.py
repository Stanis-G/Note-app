from pymongo import MongoClient
from bson import ObjectId

from modules.note import Note
from modules.lecture import Lecture


# def connect(func):
#     """Create connection to db server"""
#     def wrapper(obj, *args, **kwargs):
#         with obj.client:
#             result = func(obj, *args, **kwargs)
#         return result
#     return wrapper


class DataBase():
    """Open connection to MongoDB server, run CRUD operations on collections"""

    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name
        # self.client = MongoClient(uri)
        # self.db = self.client[db_name]


    def __enter__(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        return self.client


    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
    
    
    def create_record(self, data, collection):
        pass


    def read_record(self, collection, record_id):
        pass


    def read_record_by_name(self, name):
        pass


    def read_all(self, collection):
        pass

    
    def update_record(self, collection, record_id, new_data):
        pass


    def update_record_by_name(self, collection, record_name, new_data):
        pass


    def delete_record(self, collection, record_id):
        pass


    def delete_record_by_name(self, record_name):
        pass


class ProfileCollection(DataBase):
    """Connect to collection of users, manipulate user profiles"""

    def __init__(self, uri, db_name):
        super().__init__(uri, db_name)


    def __enter__(self):
        super().__enter__()
        self.collection = self.db['users']

    
    def create_record(self, data):
        self.collection.insert_one(data)


    def read_all(self):
        return list(self.collection.find({}))
    

    def read_record_by_name(self, name):
        return self.collection.find_one({"username": name})


class RecordCollection(DataBase):
    """Connect to collections of user records, manipulate user data"""

    def __init__(self, uri, db_name, username, collection_name):
        super().__init__(uri, db_name)
        self.user = username
        self.collection_name = collection_name


    def __enter__(self):
        super().__enter__()
        self.collection = self.db[self.collection_name]
    
    
    def create_record(self, data):
        self.collection.insert_one(data)


    def read_record(self, record_id):
        object_id = ObjectId(record_id) # wrap id to ObjectId
        return self.collection.find_one({"_id": object_id})
    

    def read_record_by_name(self, name):
        return self.collection.find_one({"header": name})


    def read_all(self):
        return list(self.collection.find({"user": self.user}))

    
    def update_record(self, record_id, new_data):
        object_id = ObjectId(record_id) # wrap id to ObjectId
        self.collection.update_one({"_id": object_id}, {"$set": new_data})


    def update_record_by_name(self, record_name, new_data):
        self.collection.update_one({"header": record_name}, {"$set": new_data})


    def delete_record(self, record_id):
        object_id = ObjectId(record_id) # wrap id to ObjectId
        self.collection.delete_one({"_id": object_id})

    
    def delete_record_by_name(self, record_name):
        self.collection.delete_one({"header": record_name})


class NoteCollection(RecordCollection):
    """Connect to collections of user records, manipulate user data"""

    def __init__(self, uri, db_name, username):
        super().__init__(uri, db_name, username, collection_name='notes')


    def read_record(self, record_id):
        record = super().read_record(record_id)
        return Note(from_db=True, **record)
    

    def read_record_by_name(self, name):
        record = super().read_record_by_name(name)
        return Note(from_db=True, **record)


    def read_all(self):
        record_lst = super().read_all()
        return [Note(from_db=True, **record) for record in record_lst]
    

    def update_record(self, record_id, new_data):
        new_data = Note(from_db=False, **new_data)
        super().update_record(record_id, new_data)


    def update_record_by_name(self, record_name, new_data):
        new_data = Note(from_db=False, **new_data)
        super().update_record_by_name(record_name, new_data)


class LectureCollection(RecordCollection):
    """Connect to collections of user records, manipulate user data"""

    def __init__(self, uri, db_name, username):
        super().__init__(uri, db_name, username, collection_name='lectures')


    def read_record(self, record_id):
        record = super().read_record(record_id)
        return Lecture(from_db=True, **record)
    

    def read_record_by_name(self, name):
        record = super().read_record_by_name(name)
        return Lecture(from_db=True, **record)


    def read_all(self):
        record_lst = super().read_all()
        return [Lecture(from_db=True, **record) for record in record_lst]


    def update_record(self, record_id, new_data):
        new_data = Lecture(from_db=False, **new_data)
        super().update_record(record_id, new_data)


    def update_record_by_name(self, record_name, new_data):
        new_data = Lecture(from_db=False, **new_data)
        super().update_record_by_name(record_name, new_data)
