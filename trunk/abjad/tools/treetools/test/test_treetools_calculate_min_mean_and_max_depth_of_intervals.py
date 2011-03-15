from fractions import Fraction
from abjad.tools.treetools._make_test_blocks import _make_test_blocks
from abjad.tools.treetools import IntervalTree
from abjad.tools.treetools import calculate_min_mean_and_max_depth_of_intervals


def test_treetools_calculate_min_mean_and_max_depth_of_intervals_01( ):
   tree = IntervalTree([ ])
   result = calculate_min_mean_and_max_depth_of_intervals(tree)
   assert result is None


def test_treetools_calculate_min_mean_and_max_depth_of_intervals_02( ):
   tree = IntervalTree(_make_test_blocks( ))
   result = calculate_min_mean_and_max_depth_of_intervals(tree)
   assert result == (0, Fraction(45, 37), 3)
