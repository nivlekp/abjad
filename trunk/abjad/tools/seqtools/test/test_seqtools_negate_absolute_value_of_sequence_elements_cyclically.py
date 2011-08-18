from abjad import *
from abjad.tools import seqtools
import py.test


def test_seqtools_negate_absolute_value_of_sequence_elements_cyclically_01():

    l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
    t = seqtools.negate_absolute_value_of_sequence_elements_cyclically(l, [0, 1, 2], 5)

    assert t == [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]


def test_seqtools_negate_absolute_value_of_sequence_elements_cyclically_02():

    assert py.test.raises(TypeError,
        "seqtools.negate_absolute_value_of_sequence_elements_cyclically('foo', [0, 1, 2])")
