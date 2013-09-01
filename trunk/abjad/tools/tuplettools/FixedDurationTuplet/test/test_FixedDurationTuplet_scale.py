# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet_scale_01():
    r'''Double tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    mutate(tuplet).scale(Multiplier(2))

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'4
            d'4
            e'4
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_02():
    r'''Halve tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    mutate(tuplet).scale(Multiplier(1, 2))

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_03():
    r'''Quadruple tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    mutate(tuplet).scale(Multiplier(4))

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'2
            d'2
            e'2
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_04():
    r'''Quarter tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    mutate(tuplet).scale(Multiplier(1, 4))

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'32
            d'32
            e'32
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_05():
    r'''Multiply tuplet by 3/2.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    mutate(tuplet).scale(Multiplier(3, 2))

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8.
            d'8.
            e'8.
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_06():
    r'''Multiply tuplet by 2/3.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    mutate(tuplet).scale(Multiplier(2, 3))

    assert testtools.compare(
        tuplet,
        r'''
        \times 8/9 {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_07():
    r'''Multiply tuplet by 3/5.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    mutate(tuplet).scale(Multiplier(3, 5))

    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_08():
    r'''Multiply undotted, unbracketted notes by 3/2; ie, add a single dot.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(3, 8), "c'8 d'8 e'8")
    mutate(tuplet).scale(Multiplier(3, 2))

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'8.
            d'8.
            e'8.
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_09():
    r'''Binary target duration.
    '''

    tuplet = tuplettools.FixedDurationTuplet(
        Duration(3, 8), [Note(0, (2, 8)), Note(0, (3, 8))])

    mutate(tuplet).scale(Multiplier(2, 3))

    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
            c'8
            c'8.
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_FixedDurationTuplet_scale_10():
    r'''Target duration without power-of-two denominator.
    '''

    tuplet = tuplettools.FixedDurationTuplet(
        Duration(4, 8), [Note(0, (2, 8)), Note(0, (3, 8))])

    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
            c'4
            c'4.
        }
        '''
        )

    mutate(tuplet).scale(Multiplier(2, 3))

    assert testtools.compare(
        tuplet,
        r'''
        \times 8/15 {
            c'4
            c'4.
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()
