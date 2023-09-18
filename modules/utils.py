class Notebook:
    
    NUMBER_OF_OBJ = 0

    def __new__(cls, *args, **kwargs):
        cls.NUMBER_OF_OBJ += 1
        return super().__new__(cls)
    
    def __init__(self, header=None):
        self.set_header(header)

    def set_header(self, header=None):
        self.header = f'{self.__class__.__name__} {self.number_of_obj()}' if not header else header

    @classmethod
    def number_of_obj(cls):
        return cls.NUMBER_OF_OBJ


class Writable(Notebook):
    """Represents objects, containing text, like Note or Lecture"""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    
    def __init__(self, header=None):
        super().__init__(header)
        self.text = None
    
    def write(self, data):
        # Этот метод должен быть переопределен в классах-наследниках
        pass


class WritableSet(Notebook):
    """Represents set of writable objects"""

    def __init__(self, header):
        self.list = []
        self.set_header(header)


    
