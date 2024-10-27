import os
from dotenv import load_dotenv
import pytest

from ..database import NoteCollection

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
