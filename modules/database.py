from pymongo import MongoClient
from bson import ObjectId


# def connect(func):
#     """Create connection to db server"""
#     def wrapper(obj, *args, **kwargs):
#         with obj.client:
#             result = func(obj, *args, **kwargs)
#         return result
#     return wrapper


class DataBase():
    """Open conection to MongoDB server, run CRUD operations"""

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
    
    
    # @connect
    def create_record(self, data, collection):
        pass


    # @connect
    def read_record(self, collection, record_id):
        pass


    # @connect
    def read_record_by_name(self, name):
        pass


    # @connect
    def read_all(self, collection):
        pass

    
    # @connect
    def update_record(self, collection, record_id, new_data):
        pass


    # @connect
    def delete_record(self, collection, record_id):
        pass


class Profiles(DataBase):
    """Open conection to MongoDB server, run CRUD operations"""

    def __init__(self, uri, db_name):
        super().__init__(uri, db_name)
        # self.collection = self.db['users']


    def __enter__(self):
        super().__enter__()
        self.collection = self.db['users']

    
    # @connect
    def create_record(self, data):
        self.collection.insert_one(data)


    # @connect
    def read_all(self):
        return list(self.collection.find({}))
    

    # @connect
    def read_record_by_name(self, name):
        return self.collection.find_one({"username": name})


class Records(DataBase):
    """Open conection to MongoDB server, run CRUD operations"""

    def __init__(self, uri, db_name, username, collection_name):
        super().__init__(uri, db_name, username)
        self.user = username
        # self.collection = self.db[collection_name]
        self.collection_name = collection_name


    def __enter__(self):
        super().__enter__()
        self.collection = self.db[self.collection_name]
    
    
    # @connect
    def create_record(self, data):
        self.collection.insert_one(data)


    # @connect
    def read_record(self, record_id):
        object_id = ObjectId(record_id) # wrap id to ObjectId
        return self.collection.find_one({"_id": object_id})
    

    # @connect
    def read_record_by_name(self, name):
        return self.collection.find_one({"header": name})


    # @connect
    def read_all(self):
        return list(self.collection.find({"user": self.user}))

    
    # @connect
    def update_record(self, record_id, new_data):
        object_id = ObjectId(record_id) # wrap id to ObjectId
        self.collection.update_one({"_id": object_id}, new_data)


    # @connect
    def delete_record(self, record_id):
        object_id = ObjectId(record_id) # wrap id to ObjectId
        self.collection.delete_one({"_id": object_id})
