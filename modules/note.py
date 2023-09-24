from .utils import Writable, WritableSet


class Note(Writable):
    """Represents notes"""

    def render(self, **kwargs):
        super().render(template_name='note.html', **kwargs)

    
class NoteSet(WritableSet):
    """Represents sets of notes"""


    
