from .utils import Writable, WritableSet, Regenerator


class Note(Writable):
    """Represents notes"""

    # def render(self, **kwargs):
    #     super().render(template_name='note.html', **kwargs)

    
class NoteSet(WritableSet):
    """Represents sets of notes"""


class NoteRegenerator(Regenerator):
    """Restore Note obj from params, loaded from database"""

    def restore(self, owner, header, text, creation_date, last_change_date):
        note = Note(owner, header)
        note.write(text)
        note.set_meta(creation_date, last_change_date)
        return note


    
