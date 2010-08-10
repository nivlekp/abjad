from abjad.tools.componenttools.iterate_namesakes_backward_from_component import iterate_namesakes_backward_from_component
from abjad.tools.componenttools.iterate_namesakes_forward_from_component import iterate_namesakes_forward_from_component


def get_nth_namesake_from_component(component, n):
   '''.. versionadded:: 1.1.2

   For positive `n`, return namesake to the right of `component`. ::

      abjad> t = Staff(macros.scale(4))
      abjad> componenttools.get_nth_namesake_from_component(t[1], 1)
      Note(e', 8)

   For negative `n`, return namesake to the left of `component`. ::

      abjad> t = Staff(macros.scale(4))
      abjad> componenttools.get_nth_namesake_from_component(t[1], -1)
      Note(c', 8)

   Return `component` when `n` is zero. ::

      abjad> t = Staff(macros.scale(4))
      abjad> componenttools.get_nth_namesake_from_component(t[1], 0)
      Note(d', 8)

   .. versionchanged:: 1.1.2
      renamed ``iterate.get_nth_namesake_from( )`` to
      ``componenttools.get_nth_namesake_from_component( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.get_nth_namesake_from_component( )`` to
      ``componenttools.get_nth_namesake_from_component( )``.
   '''

   if 0 <= n:
      for i, namesake in enumerate(iterate_namesakes_forward_from_component(component)):
         if i == n:
            return namesake
   else:
      n = abs(n)
      for i, namesake in enumerate(iterate_namesakes_backward_from_component(component)):
         if i == n:
            return namesake

   raise IndexError('only %s namesakes from %s, not %s.' % (i, component, n))
