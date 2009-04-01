from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _TupletBracketInterface(_Interface, _GrobHandler):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TupletBracket')
