from abjad.container.container import Container
from abjad.grace.formatter import _GraceFormatter


class Grace(Container):

   def __init__(self, music = None):
      music = music or None
      Container.__init__(self, music)
      self.formatter = _GraceFormatter(self)
      self.type = 'grace'

   ### OVERLOADS ###

   def __repr__(self):
      return 'Grace(%s)' % self._summary

   ### PUBLIC ATTRIBUTES ###

   @apply
   def type( ):
      def fget(self):
         return self._type
      def fset(self, arg):
         assert arg in ('after', 'grace', 'acciaccatura', 'appoggiatura')
         self._type = arg
      return property(**locals( ))
