# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_containertools_fuse_like_named_contiguous_containers_in_expr_01():
    r'''Do nothing on leaf.
    '''

    t = Note(1, (1, 4))
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert result is None
    assert isinstance(t, Note)


def test_containertools_fuse_like_named_contiguous_containers_in_expr_02():
    r'''Do not fuse unnamed voices.
    '''

    t = Staff([
        Voice(notetools.make_repeated_notes(2)), 
        Voice(notetools.make_repeated_notes(2))])
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert result is None


def test_containertools_fuse_like_named_contiguous_containers_in_expr_03():
    r'''Do not fuse differently named voices.
    '''

    t = Staff([
        Voice(notetools.make_repeated_notes(2)), 
        Voice(notetools.make_repeated_notes(2))])
    t[0].name = 'one'
    t[1].name = 'two'
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert result is None


def test_containertools_fuse_like_named_contiguous_containers_in_expr_04():
    r'''Do not fuse tuplets.
    '''

    t = Voice([
        Tuplet(Fraction(2, 3), notetools.make_repeated_notes(3)),
        Tuplet(Fraction(2, 3), notetools.make_repeated_notes(3))])
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert result is None
    assert len(t) == 2


def test_containertools_fuse_like_named_contiguous_containers_in_expr_05():
    r'''Fuse like-named staves.
    '''

    t = Staff(notetools.make_repeated_notes(4)) * 2
    t[0].name = t[1].name = 'staffOne'
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert isinstance(result, Staff)
    assert len(result) == 8


def test_containertools_fuse_like_named_contiguous_containers_in_expr_06():
    r'''Fuse like-named staves but not differently named voices.
    '''

    t = Container(Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
    t[0].name = t[1].name = 'staffOne'

    r'''
    {
        \context Staff = "staffOne" {
            \new Voice {
                c'8
                c'8
                c'8
                c'8
            }
        }
        \context Staff = "staffOne" {
            \new Voice {
                c'8
                c'8
                c'8
                c'8
            }
        }
    }
    '''

    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert isinstance(result, Container)
    assert len(result) == 1
    assert isinstance(result[0], Staff)
    assert len(result[0]) == 2
    assert isinstance(result[0][0], Voice)
    assert isinstance(result[0][1], Voice)
    assert len(result[0][0]) == 4
    assert len(result[0][1]) == 4
    assert testtools.compare(
        result.lilypond_format,
        '{\n\t\\context Staff = "staffOne" {\n\t\t\\new Voice {\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t}\n\t\t\\new Voice {\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t}\n\t}\n}'
        )

    r'''
    {
        \context Staff = "staffOne" {
            \new Voice {
                c'8
                c'8
                c'8
                c'8
            }
            \new Voice {
                c'8
                c'8
                c'8
                c'8
            }
        }
    }
    '''


def test_containertools_fuse_like_named_contiguous_containers_in_expr_07():
    r'''Fuse outside-of-score components.
    '''

    t = 2 * Voice(notetools.make_repeated_notes(4))
    t[0].name = t[1].name = 'voiceOne'
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert isinstance(result, Voice)
    assert len(result) == 8


def test_containertools_fuse_like_named_contiguous_containers_in_expr_08():
    r'''Fuse parallel voices within parallel staves within parallel
    staff groups within a single container.
    '''

    v1 = Voice(Note("c'4")*2)
    v1.name = '1'
    v2 = Voice(Note(2, (1, 4))*2)
    v2.name = '2'
    v3 = Voice(Note(4, (1, 4))*2)
    v3.name = '3'
    t1 = Staff([v1, v2, v3])
    t1.is_parallel = True
    t1.name = 'staff1'
    t2 = componenttools.copy_components_and_fracture_crossing_spanners([t1])[0]
    t2.is_parallel = True
    t2.name = 'staff2'
    t3 = componenttools.copy_components_and_fracture_crossing_spanners([t1])[0]
    t3.is_parallel = True
    t3.name = 'staff3'
    s1 = scoretools.StaffGroup([t1, t2, t3])
    s1.name = 'sg'
    s2 = componenttools.copy_components_and_fracture_crossing_spanners([s1])[0]
    s2.name = 'sg'
    s = Container([s1, s2])

    containertools.fuse_like_named_contiguous_containers_in_expr(s)
    assert len(s) == 1
    assert testtools.compare(
        s.lilypond_format,
        '{\n\t\\context StaffGroup = "sg" <<\n\t\t\\context Staff = "staff1" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t\t\\context Staff = "staff2" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t\t\\context Staff = "staff3" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t>>\n}'
        )

    r'''
    {
    \context StaffGroup = "sg" <<
        \context Staff = "staff1" <<
            \context Voice = "1" {
                c'4
                c'4
                c'4
                c'4
            }
            \context Voice = "2" {
                d'4
                d'4
                d'4
                d'4
            }
            \context Voice = "3" {
                e'4
                e'4
                e'4
                e'4
            }
        >>
        \context Staff = "staff2" <<
            \context Voice = "1" {
                c'4
                c'4
                c'4
                c'4
            }
            \context Voice = "2" {
                d'4
                d'4
                d'4
                d'4
            }
            \context Voice = "3" {
                e'4
                e'4
                e'4
                e'4
            }
        >>
        \context Staff = "staff3" <<
            \context Voice = "1" {
                c'4
                c'4
                c'4
                c'4
            }
            \context Voice = "2" {
                d'4
                d'4
                d'4
                d'4
            }
            \context Voice = "3" {
                e'4
                e'4
                e'4
                e'4
            }
        >>
    >>
    }
    '''

def test_containertools_fuse_like_named_contiguous_containers_in_expr_09():
    r'''Fuse nested parallel structures in sequence.
    '''

    v1a = Voice(Note(0, (1,4))*2)
    v1a.name = 'voiceOne'
    v1b = Voice(Note(0, (1,4))*2)
    v1b.name = 'voiceOne'
    v2a = Voice(Note(12, (1,4))*2)
    v2a.name = 'voiceTwo'
    v2b = Voice(Note(12, (1,4))*2)
    v2b.name = 'voiceTwo'
    s1 = Staff([v1a, v1b])
    s1.name ='staffOne'
    s2 = Staff([v2a, v2b])
    s2.name ='staffTwo'

    sg1 = scoretools.StaffGroup([s1, s2])
    sg1.name ='groupOne'
    sg2 = componenttools.copy_components_and_fracture_crossing_spanners([sg1])[0]
    sg2.name ='groupTwo'
    sg_g = scoretools.StaffGroup([sg1, sg2])
    sg_g.name = 'topGroup'
    seq = containertools.fuse_like_named_contiguous_containers_in_expr([sg_g, componenttools.copy_components_and_fracture_crossing_spanners([sg_g])[0]])

    assert testtools.compare(
        seq.lilypond_format,
        '\\context StaffGroup = "topGroup" <<\n\t\\context StaffGroup = "groupOne" <<\n\t\t\\context Staff = "staffOne" {\n\t\t\t\\context Voice = "voiceOne" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "staffTwo" {\n\t\t\t\\context Voice = "voiceTwo" {\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t}\n\t\t}\n\t>>\n\t\\context StaffGroup = "groupTwo" <<\n\t\t\\context Staff = "staffOne" {\n\t\t\t\\context Voice = "voiceOne" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "staffTwo" {\n\t\t\t\\context Voice = "voiceTwo" {\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t}\n\t\t}\n\t>>\n>>'
        )

    r'''
    \context StaffGroup = "topGroup" <<
        \context StaffGroup = "groupOne" <<
            \context Staff = "staffOne" {
                \context Voice = "voiceOne" {
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                }
            }
            \context Staff = "staffTwo" {
                \context Voice = "voiceTwo" {
                    c''4
                    c''4
                    c''4
                    c''4
                    c''4
                    c''4
                    c''4
                    c''4
                }
            }
        >>
        \context StaffGroup = "groupTwo" <<
            \context Staff = "staffOne" {
                \context Voice = "voiceOne" {
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                }
            }
            \context Staff = "staffTwo" {
                \context Voice = "voiceTwo" {
                    c''4
                    c''4
                    c''4
                    c''4
                    c''4
                    c''4
                    c''4
                    c''4
                }
            }
        >>
    >>
    '''


def test_containertools_fuse_like_named_contiguous_containers_in_expr_10():
    r'''Fuse containers.
    '''

    t1 = Container(Note("c'4")*2)
    t2 = Container(Note("c'4")*2)
    tadd = containertools.fuse_like_named_contiguous_containers_in_expr(
        [t1, t2])
    assert testtools.compare(
        tadd.lilypond_format,
        "{\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
        )
    assert select(tadd).is_well_formed()


def test_containertools_fuse_like_named_contiguous_containers_in_expr_11():
    r'''Fuse sequentially nested like-named voices.
    '''

    t1 = Staff([Voice(Note("c'4")*2)])
    t2 = Staff([Voice(Note("c'4")*2)])
    t1[0].name = t2[0].name = 'voiceOne'
    t1.name = t2.name = 'staffOne'
    tadd = containertools.fuse_like_named_contiguous_containers_in_expr([
        t1, t2])
    assert isinstance(tadd, Staff)
    assert len(tadd) == 1
    assert isinstance(tadd[0], Voice)
    assert len(tadd[0]) == 4
    assert testtools.compare(
        tadd.lilypond_format,
        '\\context Staff = "staffOne" {\n\t\\context Voice = "voiceOne" {\n\t\tc\'4\n\t\tc\'4\n\t\tc\'4\n\t\tc\'4\n\t}\n}'
        )

    r'''
    \context Staff = "staffOne" {
        \context Voice = "voiceOne" {
            c'4
            c'4
            c'4
            c'4
        }
    }
    '''


def test_containertools_fuse_like_named_contiguous_containers_in_expr_12():
    r'''Fuse matching parallel containers with like-named voices.
    '''

    t1 = Container([Voice(Note("c'4")*2)])
    t1.is_parallel = True
    t2 = Container([Voice(Note("c'4")*2)])
    t2.is_parallel = True
    t1[0].name = t2[0].name = 'voiceOne'
    tadd = containertools.fuse_like_named_contiguous_containers_in_expr(
        [t1, t2])

    r'''
    <<
        \context Voice = "voiceOne" {
            c'4
            c'4
            c'4
            c'4
        }
    >>
    '''

    assert select(tadd).is_well_formed()
    assert isinstance(tadd, Container)
    assert tadd.is_parallel
    assert len(tadd) == 1
    assert isinstance(tadd[0], Voice)
    assert len(tadd[0]) == 4


def test_containertools_fuse_like_named_contiguous_containers_in_expr_13():
    r'''Fuse matching parallel containers with two like-named voices each.
    '''


    v1 = Voice(Note("c'4")*2)
    v1.name = '1'
    v2 = Voice(Note(1, (1, 4))*2)
    v2.name = '2'
    v3 = Voice(Note("c'4")*2)
    v3.name = '1'
    v4 = Voice(Note(1, (1, 4))*2)
    v4.name = '2'
    t1 = Staff([v1, v2])
    t1.is_parallel = True
    t2 = Staff([v3, v4])
    t2.is_parallel = True
    t1.name = t2.name = 'staffOne'
    tadd = containertools.fuse_like_named_contiguous_containers_in_expr(
        [t1, t2])

    r'''
    \context Staff = "staffOne" <<
        \context Voice = "1" {
            c'4
            c'4
            c'4
            c'4
        }
        \context Voice = "2" {
            cs'4
            cs'4
            cs'4
            cs'4
        }
    >>
    '''

    assert isinstance(tadd, Staff)
    assert tadd.is_parallel
    assert len(tadd) == 2
    assert isinstance(tadd[0], Voice)
    assert isinstance(tadd[1], Voice)
    assert len(tadd[0]) == 4
    assert len(tadd[1]) == 4
    assert tadd[0].name == '1'
    assert tadd[1].name == '2'
    assert tadd.name == 'staffOne'
