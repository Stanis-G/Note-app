from datetime import datetime
from flask import session
from markdown import markdown


class RecordObject(dict):


    def __init__(self, from_db=False, **kwargs):
        super().__init__(**kwargs)
        self.from_db = from_db # True means that object is being restored from db
        self.set_creation_date()
        self.set_last_change_date()
        self.set_header()


    def set_creation_date(self):
        """Assign creation date if not passed"""
        if 'creation_date' not in self:
            current_data = str(datetime.now()).split('.')[0]
            self.__setitem__('creation_date', current_data)


    def set_last_change_date(self):
        """Assign last change date to current date"""
        # If data is just created
        is_data_new = not self.from_db
        # If data restored from db, but last_change_date is missing
        is_field_miss = self.from_db and 'last_change_date' not in self
        if is_data_new or is_field_miss:
            current_data = str(datetime.now()).split('.')[0]
            self.__setitem__('last_change_date', current_data)
            


    def set_header(self):
        if 'header' not in self:
            raise Exception('Header is not defined') # Change to custom exception
            


class Record(RecordObject):
    """Contains one record data and metainfo"""
    
    # def __init__(self, from_db=False, **kwargs):
    #     super().__init__(from_db, **kwargs)
        # self.render()


    # def render(self):
    #     """Render text markdown syntax to html"""
    #     text = self.get('text') or ''
    #     text = markdown(text)
    #     self.__setitem__('text', text)
        
    
    # def write(self, data):
    #     """Write data"""
    #     self.content = data


    def set_content(self):
        """Assign content"""
        if 'content' not in self:
            self.__setitem__('content', '')


class RecordSet(RecordObject):
    """Represents set of records"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_records_lst()
        

    # def create_child(self, header):
    #     """Create new Record instance"""
    #     child = Record(header)
    #     self.list.append(child)


    def set_records_lst(self):
        """Assign records lst"""
        if 'records' not in self:
            self.__setitem__('records', [])


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
