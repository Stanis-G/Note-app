from pymongo import MongoClient

from modules.note import Note
from modules.lecture import Lecture


class DataBase():
    """Open connection to MongoDB server, run CRUD operations on collections"""

    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name


    def __enter__(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        return self.client


    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
    
    
    def create_record(self, data, collection):
        pass


    def read_record_by_name(self, name):
        pass


    def read_all(self, collection):
        pass


    def update_record_by_name(self, collection, record_name, new_data):
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

    def __init__(self, uri, db_name, username, collection_name, test_mode=False):
        super().__init__(uri, db_name)
        self.user = username
        self.collection_name = collection_name
        self.test_mode = test_mode


    def __enter__(self):
        super().__enter__()
        self.collection = self.db[self.collection_name]

    def __exit__(self, exc_type, exc_value, traceback):
        if self.test_mode:
            self.collection.delete_many({})
        return super().__exit__(exc_type, exc_value, traceback)
    
    
    def create_record(self, data):
        self.collection.insert_one(data)
    

    def read_record_by_name(self, name):
        return self.collection.find_one({"header": name})


    def read_all(self):
        return list(self.collection.find({"username": self.user}))


    def update_record_by_name(self, record_name, new_data):
        if 'header' in new_data and new_data['header'] != record_name:
            # Create new record if new header passed
            data = self.read_record_by_name(record_name)
            self.delete_record_by_name(record_name)
            data.pop('_id')
            data.update(new_data)
            self.create_record(new_data)
        else:
            # Update existing record if header is not changed
            new_data.update({'header': record_name})
            self.collection.update_one({"header": record_name}, {"$set": new_data})

    
    def delete_record_by_name(self, record_name):
        self.collection.delete_one({"header": record_name})


class NoteCollection(RecordCollection):
    """Connect to collections of user records, manipulate user data"""

    def __init__(self, uri, db_name, username, test_mode=False):
        super().__init__(uri, db_name, username, collection_name='notes', test_mode=test_mode)


    def create_record(self, data):
        data = Note(from_db=False, **data)
        super().create_record(data)
    

    def read_record_by_name(self, name):
        record = super().read_record_by_name(name)
        return Note(from_db=True, **record)


    def read_all(self):
        record_lst = super().read_all()
        return [Note(from_db=True, **record) for record in record_lst]


    def update_record_by_name(self, record_name, new_data):
        new_data = Note(from_db=False, **new_data)
        super().update_record_by_name(record_name, new_data)


class LectureCollection(RecordCollection):
    """Connect to collections of user records, manipulate user data"""

    def __init__(self, uri, db_name, username, test_mode=False):
        super().__init__(uri, db_name, username, collection_name='lectures', test_mode=test_mode)


    def create_record(self, data):
        data = Lecture(from_db=False, **data)
        super().create_record(data)
    

    def read_record_by_name(self, name):
        record = super().read_record_by_name(name)
        return Lecture(from_db=True, **record)


    def read_all(self):
        record_lst = super().read_all()
        return [Lecture(from_db=True, **record) for record in record_lst]


    def update_record_by_name(self, record_name, new_data):
        new_data = Lecture(from_db=False, **new_data)
        super().update_record_by_name(record_name, new_data)
