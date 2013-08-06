# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_Measure_extend_01():
    r'''Do not adjust time signature automatically.
    '''

    measure = Measure((3, 4), "c' d' e'")
    measure.extend("f' g'")

    assert measure.is_overfull
    assert py.test.raises(Exception, 'f(measure)')


def test_Measure_extend_02():
    r'''Adjust time signature automatically.
    '''

    measure = Measure((3, 4), "c' d' e'")
    measure.automatically_adjust_time_signature = True
    measure.extend("f' g'")

    assert not measure.is_misfilled
    assert testtools.compare(
        measure.lilypond_format,
        "{\n\t\\time 5/4\n\tc'4\n\td'4\n\te'4\n\tf'4\n\tg'4\n}"
        )
