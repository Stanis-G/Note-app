from datetime import datetime
from flask import session


class WritableObject:
    
    NUMBER_OF_OBJ = 0

    def __new__(cls, *args, **kwargs):
        cls.NUMBER_OF_OBJ += 1
        return super().__new__(cls)
    
    def __init__(self, owner, header=None):
        self.set_header(header)
        self.meta = dict(
            creation_date=str(datetime.now().date()),
            last_change_date=str(datetime.now().date()),
            owner=owner,
        )

    def set_meta(self, creation_date, last_change_date):
        self.meta.update(dict(
            creation_date=creation_date,
            last_change_date=last_change_date,
        ))

    def set_header(self, header=None):
        self.header = f'{self.__class__.__name__} {self.number_of_obj()}' if not header else header

    @classmethod
    def number_of_obj(cls):
        return cls.NUMBER_OF_OBJ


class Writable(WritableObject):
    """Represents objects, containing text, like Note or Lecture"""
    
    def __init__(self, owner, header=None):
        super().__init__(owner, header)
        self.text = None
    
    def write(self, data):
        """Write data"""
        self.text = data


class WritableSet(WritableObject):
    """Represents set of writable objects"""

    def __init__(self, owner, header=None):
        super().__init__(header)
        self.list = []
        
    def create_child(self, header):
        """Create new Writable instance"""
        child = Writable(header)
        self.list.append(child)


class Regenerator:

    def restore(self):
        pass




def set_menu():
    menu = [
        {'name': 'Главная', 'url': '/index'},
        {'name': 'О приложении', 'url': '/about'},
        {'name': 'Обратная связь', 'url': '/contact'},
    ]
    if 'userLogged' in session:
        #menu.append({'name': session['userLogged'], 'url': f'/profile/{session["userLogged"]}'})
        menu.append({'name': 'Выход', 'url': '/logout'})
    else:
        menu.append({'name': 'Вход', 'url': '/login'})
    return menu


def is_user_logged():
    return None if 'userLogged' not in session else session['userLogged']
