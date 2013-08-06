# -*- encoding: utf-8 -*-
from abjad import *


def test_Tuplet_from_duration_and_ratio_01():

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/2 {\n\tc'8\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/2 {\n\tc'16\n\tc'16\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16\n\tc'16\n\tc'16\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1, 1], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/2 {\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1, 1, 1], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/5 {\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n}"
        )


def test_Tuplet_from_duration_and_ratio_02():

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/2 {\n\tc'8\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16\n\tc'8\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3, 3], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"
        )


def test_Tuplet_from_duration_and_ratio_03():
    r'''Interpret negative proportions as rests.
    '''

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1, -2, -2, 3, 3], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 12/11 {\n\tc'64\n\tr32\n\tr32\n\tc'32.\n\tc'32.\n}"
        )


def test_Tuplet_from_duration_and_ratio_04():
    r'''Reduce proportions relative to each other.
    '''

    duration = Fraction(3, 16)

    t1 = Tuplet.from_duration_and_ratio(
        duration, [1, -2, -2, 3, 3], avoid_dots=True, is_diminution=False)
    t2 = Tuplet.from_duration_and_ratio(
        duration, [2, -4, -4, 6, 6], avoid_dots=True, is_diminution=False)
    assert t1.lilypond_format == t2.lilypond_format

    t = Tuplet.from_duration_and_ratio(
        Fraction(1, 8), [27], avoid_dots=True, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'8\n}"
        )


def test_Tuplet_from_duration_and_ratio_05():

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'8.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16.\n\tc'16.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16\n\tc'16\n\tc'16\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1, 1], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1, 1, 1], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 8/5 {\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n}"
        )


def test_Tuplet_from_duration_and_ratio_06():

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'8.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16\n\tc'8\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 8/5 {\n\tc'64.\n\tc'32.\n\tc'32.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3, 3], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"
        )


def test_Tuplet_from_duration_and_ratio_07():
    r'''Reduce proportions relative to each other.
    '''

    duration = Fraction(3, 16)

    t1 = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3, 3], avoid_dots=False, is_diminution=False)
    t2 = Tuplet.from_duration_and_ratio(
        duration, [2, 4, 4, 6, 6], avoid_dots=False, is_diminution=False)
    assert t1.lilypond_format == t2.lilypond_format

    t = Tuplet.from_duration_and_ratio(
        Fraction(1, 8), [27], avoid_dots=False, is_diminution=False)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'8\n}"
        )


def test_Tuplet_from_duration_and_ratio_08():

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/4 {\n\tc'4\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/4 {\n\tc'8\n\tc'8\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16\n\tc'16\n\tc'16\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1, 1], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/4 {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1, 1, 1], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/5 {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"
        )


def test_Tuplet_from_duration_and_ratio_09():

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/4 {\n\tc'4\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16\n\tc'8\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/5 {\n\tc'16\n\tc'8\n\tc'8\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/4 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3, 3], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/11 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n\tc'16.\n}"
        )


def test_Tuplet_from_duration_and_ratio_10():
    r'''Interpret negative proportions as rests.
    '''

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1, -2, -2, 3, 3], avoid_dots=True, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/11 {\n\tc'32\n\tr16\n\tr16\n\tc'16.\n\tc'16.\n}"
        )


def test_Tuplet_from_duration_and_ratio_11():
    r'''Reduce propotions relative to each other.
    '''

    duration = Fraction(3, 16)

    t1 = Tuplet.from_duration_and_ratio(
        duration, [1, -2, -2, 3, 3], avoid_dots=True, is_diminution=True)
    t2 = Tuplet.from_duration_and_ratio(
        duration, [2, -4, -4, 6, 6], avoid_dots=True, is_diminution=True)
    assert t1.lilypond_format == t2.lilypond_format

    t = Tuplet.from_duration_and_ratio(
        Fraction(1, 8), [27])
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'8\n}"
        )


def test_Tuplet_from_duration_and_ratio_12():

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'8.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16.\n\tc'16.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16\n\tc'16\n\tc'16\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1, 1], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 1, 1, 1, 1], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\times 4/5 {\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"
        )


def test_Tuplet_from_duration_and_ratio_13():

    duration = Fraction(3, 16)

    t = Tuplet.from_duration_and_ratio(
        duration, [1], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'8.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'16\n\tc'8\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\times 4/5 {\n\tc'32.\n\tc'16.\n\tc'16.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/4 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n}"
        )

    t = Tuplet.from_duration_and_ratio(
        duration, [1, 2, 2, 3, 3], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/11 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n\tc'16.\n}"
        )


def test_Tuplet_from_duration_and_ratio_14():
    r'''Reduce proportions relative to each other.
    '''

    duration = Fraction(3, 16)

    t1 = Tuplet.from_duration_and_ratio(
        duration, [1, -2, -2, 3, 3], avoid_dots=False, is_diminution=True)
    t2 = Tuplet.from_duration_and_ratio(
        duration, [2, -4, -4, 6, 6], avoid_dots=False, is_diminution=True)
    assert t1.lilypond_format == t2.lilypond_format

    t = Tuplet.from_duration_and_ratio(
        Fraction(1, 8), [27], avoid_dots=False, is_diminution=True)
    assert testtools.compare(
        t.lilypond_format,
        "{\n\tc'8\n}"
        )


def test_Tuplet_from_duration_and_ratio_15():
    r'''Coerce duration.
    '''

    tuplet = Tuplet.from_duration_and_ratio(
        (1, 4), [1, -1, 1], avoid_dots=True, is_diminution=True)

    assert testtools.compare(
        tuplet.lilypond_format,
        "\\times 2/3 {\n\tc'8\n\tr8\n\tc'8\n}"
        )
