from abjad import *
import py.test


def test_componenttools_get_preprolated_duration_of_components_01( ):
   '''Return sum of preprolated duration of components in list.'''
   
   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))

   assert componenttools.get_preprolated_duration_of_components(t[:]) == Rational(3, 8)


def test_componenttools_get_preprolated_duration_of_components_02( ):
   '''Return zero for empty list.'''

   assert componenttools.get_preprolated_duration_of_components([ ]) == Rational(0)
