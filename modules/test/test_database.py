import os
from dotenv import load_dotenv
from pymongo import MongoClient
import pytest

from ..database import NoteCollection
from ..note import Note

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB_TEST")


@pytest.fixture
def note():

    note = {
        'username': 'user_test',
        'header': 'header_test',
        'text': 'text_test',
    }
    
    return note


@pytest.fixture
def db_note(note):
    return NoteCollection(MONGO_URI, MONGO_DB, note['username'], test_mode=True)


def test_create_record_read_record_by_name(note, db_note):
    """Test methods create_record and read_record_by_name"""

    with db_note:
        db_note.create_record(note)
        note_read = db_note.read_record_by_name(note['header'])

    for key, value in note.items():
        assert value == note_read[key]


def test_read_all(note, db_note):
    """Test read_all method"""

    with db_note:
        db_note.create_record(note)
        notes = db_note.read_all()

    note_read = [i for i in notes if i['header'] == note['header']][0]
    for key, value in note.items():
        assert value == note_read[key]


@pytest.mark.parametrize("header", [None, 'header_test', 'header_update'])
def test_update_record_by_name(note, header, db_note):
    """Test update_record_by_name method"""
    update_data = dict(text="user_text_updated")

    if not header:
        with db_note and pytest.raises(Exception, match=r".*Header is not defined.*"):
            db_note.create_record(update_data)

    else:
        update_data.update({'header': header})
        with db_note:
            db_note.create_record(note)
            db_note.update_record_by_name(note['header'], update_data)
            note_read = db_note.read_record_by_name(update_data['header'])
        
        assert note_read['text'] == update_data['text']
        assert note_read['header'] == update_data['header']
