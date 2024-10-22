from datetime import datetime
from flask import session


class RecordObject:
    
    NUMBER_OF_OBJ = 0

    def __new__(cls, *args, **kwargs):
        cls.NUMBER_OF_OBJ += 1
        return super().__new__(cls)
    

    def __init__(self, owner, header=None):
        self.set_header(header)
        self.creation_date=str(datetime.now()).split('.')[0]
        self.last_change_date=str(datetime.now()).split('.')[0]
        self.owner=owner


    def set_header(self, header=None):
        self.header = f'{self.__class__.__name__} {self.number_of_obj()}' if not header else header


    @classmethod
    def number_of_obj(cls):
        return cls.NUMBER_OF_OBJ
    

    @classmethod
    def restore_from_db(cls, db_params):
        """Restore obj by params dict from db"""
        note = cls(db_params['owner'], db_params['header'])
        note.creation_date = db_params['creation_date']
        note.last_change_date = db_params['last_change_date']
        note.write(db_params['content'])
        return note
        


class Record(RecordObject):
    """Represents objects with content like Note or Lecture"""
    
    def __init__(self, owner, header=None):
        super().__init__(owner, header)
        self.content = None
    
    def write(self, data):
        """Write data"""
        self.content = data


class RecordSet(RecordObject):
    """Represents set of records"""

    def __init__(self, owner, header=None):
        super().__init__(header)
        self.list = []
        
    def create_child(self, header):
        """Create new Record instance"""
        child = Record(header)
        self.list.append(child)


def set_menu():
    menu = [
        {'name': 'Главная', 'url': '/main'},
        {'name': 'О приложении', 'url': '/about'},
        {'name': 'Обратная связь', 'url': '/contact'},
    ]
    if 'username' in session:
        menu.append({'name': 'Выход', 'url': '/logout'})
    else:
        menu.append({'name': 'Вход', 'url': '/login'})
    return menu


def error_replacer(error, replacement_error):
    """Decorator for exceptions replace"""
    def wrapper_ext(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except error:
                raise replacement_error
            return result
        return wrapper
    return wrapper_ext
