from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def calculate_min_mean_and_max_magnitude_of_intervals(intervals):
   '''Return a 3-tuple of the minimum, mean and maximum magnitude of all intervals in `intervals`.
   If `intervals` is empty, return None.
   '''

   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree:
      return None
   
   magnitudes = [x.magnitude for x in tree]
   return (min(magnitudes), Fraction(sum(magnitudes), len(magnitudes)), max(magnitudes))
