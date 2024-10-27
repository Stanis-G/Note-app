import pytest
from ..note import Note


def test_init(note):
    note = Note(**note)
    assert 'creation_date' in note
    assert 'last_change_date' in note
