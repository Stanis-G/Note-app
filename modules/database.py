import sqlite3 as sq
from datetime import datetime

from modules.note import Note
from modules.utils import error_replacer, NameExistsError


def connect(func):
    """Create connection to db"""
    def wrapper(obj, *args, **kwargs):
        with sq.connect(obj.db_path) as conn:
            obj.add_connection(conn)
            result = func(obj, *args, **kwargs)
        return result
    return wrapper


class DBObject:

    def __init__(self, db_path):
        self.db_path = db_path
        self.sql_folder = './sql/'

    def add_connection(self, connection):
        """Add connection attributes"""
        self.conn = connection
        self.conn.row_factory = sq.Row
        self.cur = self.conn.cursor()

class DataBase(DBObject):

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


class TableProfile(DBObject):

    def __init__(self, db_path):
        super().__init__(db_path)
        self.table = 'profiles'

    @connect
    def create_profile(self, login, username, password):
        """Create profile to db"""
        script = f'INSERT INTO {self.table} (login, username, password, creation_date) VALUES (?, ?, ?, ?)'
        values = (
            login,
            username,
            password,
            str(datetime.now()).split('.')[0],
        )
        self.cur.execute(script, values)

    @connect
    def get_usernames(self):
        """Return list of all registered users"""
        script = 'SELECT username FROM profiles'
        self.cur.execute(script)
        result = self.cur.fetchall()
        return [list(dict(i).values())[0] for i in result]
    

    @connect
    def get_profile(self, username):
        """Return profile data by username"""
        script = f'SELECT * FROM {self.table} WHERE username = ?'
        values = (username, )
        self.cur.execute(script, values)
        result = self.cur.fetchall()
        print(result)
        return dict(result[0])


class TableWritable(DBObject):

    def __init__(self, db_path, username):
        super().__init__(db_path)
        self.user = username

    def set_table(self, table):
        """Set table name"""
        self.table = table

    @connect
    def get_obj_params_by_header(self, header):
        """Get obj params from db by header"""
        script = f'SELECT * FROM {self.table} WHERE owner = ? and header = ?'
        values = (self.user, header)
        self.cur.execute(script, values)
        obj_params = self.cur.fetchall()
        try:
            obj_params = dict(obj_params[0])
        except IndexError:
            raise ValueError(f'Header "{header}" does not exist')
        return obj_params

    @connect
    def get_all_obj_params(self):
        """Get all obj params for current owner"""
        script = f'SELECT * FROM {self.table} WHERE owner = ?'
        values = (self.user, )
        self.cur.execute(script, values)
        all_obj_params = self.cur.fetchall()
        return all_obj_params
    
    @connect
    def delete(self, header):
        """Delete obj from db"""
        script = f'DELETE FROM {self.table} WHERE header = ?'
        values = (header, )
        self.cur.execute(script, values)


class TableNotes(TableWritable):
    """Class for interaction with table with notes"""

    def __init__(self, db_path, username):
        super().__init__(db_path, username)
        super().set_table('notebooks')


    @connect
    @error_replacer(sq.IntegrityError, NameExistsError)
    def save_note(self, note):
        """Save new note to db"""
        script = f'INSERT INTO {self.table} (header, content, creation_date, last_change_date, owner) VALUES (?, ?, ?, ?, ?)'
        values = (
            note.header,
            note.content,
            note.creation_date,
            note.last_change_date,
            note.owner,
        )
        self.cur.execute(script, values)


    def get_note_by_header(self, header):
        """Restore note from db by header"""
        note_params = super().get_obj_params_by_header(header)
        note = Note.restore_from_db(note_params)
        return note
    

    def get_all_notes(self):
        """Restore all notes from db for current user"""
        all_notes_params = super().get_all_obj_params()
        notes_lst = []
        for note_params in all_notes_params:
            note_params = dict(note_params)
            note = Note.restore_from_db(note_params)
            notes_lst.append(note)
        notes_lst.sort(key=lambda note: note.creation_date, reverse=True)
        return notes_lst


    @connect
    def update_note(self, header_old, note_new):
        """Update data in existing note"""
        script = f'UPDATE {self.table} SET header = ?, content = ?, last_change_date = ? WHERE header = ?'
        values = (
            note_new.header,
            note_new.content,
            str(datetime.now()).split('.')[0],
            header_old,
        )
        self.cur.execute(script, values)
