from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


ENV = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

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

    def set_header(self, header=None):
        self.header = f'{self.__class__.__name__} {self.number_of_obj()}' if not header else header

    @classmethod
    def number_of_obj(cls):
        return cls.NUMBER_OF_OBJ


class Writable(WritableObject):
    """Represents objects, containing text, like Note or Lecture"""
    
    def __init__(self, header=None):
        super().__init__(header)
        self.text = None
    
    def write(self, data):
        """Write data"""
        self.text = data

    def render(self, template_name, **kwargs):
        template = ENV.get_template(template_name)
        print(template.render(**kwargs))


class WritableSet(WritableObject):
    """Represents set of writable objects"""

    def __init__(self, header=None):
        super().__init__(header)
        self.list = []
        
    def create_child(self, header):
        """Create new Writable instance"""
        child = Writable(header)
        self.list.append(child)


