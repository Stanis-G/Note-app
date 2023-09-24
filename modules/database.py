import sqlite3 as sq


class DataBase:

    def __init__(self, path):
        self.path = path
        self.sql_folder = './sql/'

    
    def connect(func):
        """Create connection to db"""
        def wrapper(self, *args, **kwargs):
            with sq.connect(self.path) as conn:
                self.conn = conn
                self.conn.row_factory = sq.Row
                self.cur = self.conn.cursor()
                result = func(self, *args, **kwargs)
            return result
        return wrapper
    
    def execute_by_header__(self, header, script):
        """Execute script using header only"""
        self.cur.execute(script, (header, ))
        return self.cur.fetchall()

    @connect
    def create_db(self):
        with open(self.sql_folder + 'create_db.sql', mode='r') as f:
            self.cur.executescript(f.read())

    @connect
    def write(self, notebook):
        """Write data to db"""
        script = 'INSERT INTO notebooks (header, text, creation_date, last_change_date) VALUES (?, ?, ?, ?)'
        values = (
            notebook.header,
            notebook.text,
            *notebook.meta.values(),
        )
        self.cur.execute(script, values)

    @connect
    def get(self, header):
        """Get data from db by header"""
        script = 'SELECT * FROM notebooks WHERE header = ?'
        self.cur.execute(script, (header, ))
        result = self.cur.fetchall()
        try:
            return dict(result[0])
        except IndexError:
            raise ValueError(f'Header "{header}" does not exist')
    
    @connect
    def delete(self, header):
        """Delete row"""
        script = 'DELETE FROM notebooks WHERE header = ?'
        self.cur.execute(script, (header, ))







