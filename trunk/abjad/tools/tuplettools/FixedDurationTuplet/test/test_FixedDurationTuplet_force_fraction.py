# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet_force_fraction_01():

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t.force_fraction = True

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}"
        )
