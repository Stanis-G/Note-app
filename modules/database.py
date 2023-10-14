import sqlite3 as sq
from datetime import datetime

from modules.note import Note, NoteRegenerator


def connect(func):
    """Create connection to db"""
    def wrapper(obj, *args, **kwargs):
        with sq.connect(obj.path) as conn:
            obj.add_connection(conn)
            result = func(obj, *args, **kwargs)
        return result
    return wrapper


class DataBase:

    def __init__(self, path):
        self.path = path
        self.sql_folder = './sql/'

    def add_connection(self, connection):
        """Add connection attributes"""
        self.conn = connection
        self.conn.row_factory = sq.Row
        self.cur = self.conn.cursor()

    @connect
    def create_db__(self):
        with open(self.sql_folder + 'create_db.sql', mode='r') as f:
            self.cur.executescript(f.read())

    @connect
    def select_data_(self, table):
        """Test function for watching db data"""
        script = f'SELECT * FROM {table} LIMIT 10'
        self.cur.execute(script)
        result = self.cur.fetchall()
        return dict(result[0])
    
    @connect
    def drop_table_(self, table):
        """Delete table"""
        script = f'DROP TABLE {table}'
        self.cur.execute(script)


class TableWritable(DataBase):

    def __init__(self, path, username):
        super().__init__(path)
        self.user = username

    @connect
    def save_new(self, notebook):
        """Save new notebook to db"""
        script = 'INSERT INTO notebooks (header, text, creation_date, last_change_date, owner) VALUES (?, ?, ?, ?, ?)'
        values = (
            notebook.header,
            notebook.text,
            *notebook.meta.values(),
        )
        self.cur.execute(script, values)

    @connect
    def get_note(self, header):
        """Get one note from db by header"""
        script = 'SELECT * FROM notebooks WHERE owner = ? and header = ?'
        self.cur.execute(script, (self.user, header))
        note_params = self.cur.fetchall()
        try:
            note_params = dict(note_params[0])
        except IndexError:
            raise ValueError(f'Header "{header}" does not exist')
        note = NoteRegenerator().restore(
            note_params['owner'],
            note_params['header'],
            note_params['text'],
            note_params['creation_date'],
            note_params['last_change_date'],
        )
        return note

    @connect
    def get_all_notes(self):
        """Get all notes for current owner"""
        script = 'SELECT * FROM notebooks WHERE owner = ?'
        self.cur.execute(script, (self.user, ))
        result = self.cur.fetchall()
        return [dict(note) for note in result]
    
    @connect
    def delete(self, header):
        """Delete row"""
        script = 'DELETE FROM notebooks WHERE header = ?'
        self.cur.execute(script, (header, ))

    @connect
    def update_existing(self, header_old, notebook_new):
        """Update existing notebook"""
        script = 'UPDATE notebooks SET header = ?, text = ?, last_change_date = ? WHERE header = ?'
        self.cur.execute(script, (
            notebook_new.header,
            notebook_new.text,
            str(datetime.now().date()),
            header_old,
        ))


class TableProfile(DataBase):

    def __init__(self, path):
        super().__init__(path)
        self.table = 'profiles'

    @connect
    def create_profile(self, login, password):
        """Create profile to db"""
        script = f'INSERT INTO {self.table} (login, password, creation_date) VALUES (?, ?, ?)'
        values = (
            login,
            password,
            str(datetime.now().date()),
        )
        self.cur.execute(script, values)

    @connect
    def get_logins(self):
        """Return list of all registered logins"""
        script = 'SELECT login FROM profiles'
        self.cur.execute(script)
        result = self.cur.fetchall()
        return [list(dict(i).values())[0] for i in result]
    

    @connect
    def get_profile(self, login):
        """Return profile data by login"""
        script = f'SELECT * FROM profiles WHERE login = "{login}"'
        self.cur.execute(script)
        result = self.cur.fetchall()
        return dict(result[0])

        
        
