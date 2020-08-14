import pytest

import abjad


def test_mutate_fuse_01():
    """
    Works with list of leaves.
    """

    notes = abjad.Selection(
        [
            abjad.Note("c'4"),
            abjad.Note("c'4"),
            abjad.Note("c'4"),
            abjad.Note("c'4"),
            abjad.Note("c'4"),
            abjad.Note("c'4"),
            abjad.Note("c'4"),
            abjad.Note("c'4"),
        ]
    )
    fused = abjad.mutate.fuse(notes)

    assert len(fused) == 1
    assert fused[0].written_duration == abjad.Duration(2)


def test_mutate_fuse_02():
    """
    Works with Leaf component.
    """

    fused = abjad.mutate.fuse(abjad.Note("c'4"))
    assert len(fused) == 1
    assert fused[0].written_duration == abjad.Duration(1, 4)


def test_mutate_fuse_03():
    """
    Works with containers.
    """

    voice = abjad.Voice("c'4 c'4 c'4 c'4 c'4 c'4 c'4 c'4")
    fused = abjad.mutate.fuse(voice[:])
    assert len(fused) == 1
    assert fused[0].written_duration == 2
    assert voice[0] is fused[0]


def test_mutate_fuse_04():
    """
    Fusion results in tied notes.
    """

    voice = abjad.Voice([abjad.Note(0, (2, 16)), abjad.Note(9, (3, 16))])
    abjad.mutate.fuse(voice[:])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'4
            ~
            c'16
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_fuse_05():
    """
    Fuses leaves with differing LilyPond multipliers.
    """

    staff = abjad.Staff([abjad.Skip((1, 1)), abjad.Skip((1, 1))])
    staff[0].multiplier = (1, 16)
    staff[1].multiplier = (5, 16)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            s1 * 1/16
            s1 * 5/16
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.get.duration(staff) == abjad.Duration(3, 8)

    abjad.mutate.fuse(staff[:])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            s1 * 3/8
        }
        """
    )

    assert abjad.get.duration(staff) == abjad.Duration(3, 8)
    assert abjad.wf.wellformed(staff)


def test_mutate_fuse_06():
    """
    Fuses two unincorporated tuplets with same multiplier.
    """

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    abjad.beam(tuplet_1[:])
    tuplet_2 = abjad.Tuplet((2, 3), "c'16 d'16 e'16")
    abjad.slur(tuplet_2[:])

    assert abjad.lilypond(tuplet_1) == abjad.String.normalize(
        r"""
        \times 2/3 {
            c'8
            [
            d'8
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(tuplet_1))

    assert abjad.lilypond(tuplet_2) == abjad.String.normalize(
        r"""
        \times 2/3 {
            c'16
            (
            d'16
            e'16
            )
        }
        """
    ), print(abjad.lilypond(tuplet_2))

    tuplets = abjad.select([tuplet_1, tuplet_2])
    new = abjad.mutate.fuse(tuplets)

    assert abjad.lilypond(new) == abjad.String.normalize(
        r"""
        \times 2/3 {
            c'8
            [
            d'8
            e'8
            ]
            c'16
            (
            d'16
            e'16
            )
        }
        """
    ), print(abjad.lilypond(new))

    assert len(tuplet_1) == 0
    assert len(tuplet_2) == 0
    assert new is not tuplet_1 and new is not tuplet_2
    assert abjad.wf.wellformed(new)


def test_mutate_fuse_07():
    """
    Fuses tuplets with same multiplier in score.
    """

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    abjad.beam(tuplet_1[:])
    tuplet_2 = abjad.Tuplet((2, 3), "c'16 d'16 e'16")
    abjad.slur(tuplet_2[:])
    voice = abjad.Voice([tuplet_1, tuplet_2])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
            }
            \times 2/3 {
                c'16
                (
                d'16
                e'16
                )
            }
        }
        """
    ), print(abjad.lilypond(voice))

    tuplets = voice[:]
    abjad.mutate.fuse(tuplets)

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
                c'16
                (
                d'16
                e'16
                )
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_fuse_08():
    """
    Fuses fixed-multiplier tuplets with same multiplier in score.
    """

    tuplet_1 = abjad.Tuplet(abjad.Multiplier(2, 3), "c'8 d'8 e'8")
    abjad.beam(tuplet_1[:])
    tuplet_2 = abjad.Tuplet(abjad.Multiplier(2, 3), "c'8 d'8 e'8 f'8 g'8")
    abjad.slur(tuplet_2[:])
    voice = abjad.Voice([tuplet_1, tuplet_2])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                (
                d'8
                e'8
                f'8
                g'8
                )
            }
        }
        """
    ), print(abjad.lilypond(voice))

    tuplets = voice[:]
    abjad.mutate.fuse(tuplets)

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                [
                d'8
                e'8
                ]
                c'8
                (
                d'8
                e'8
                f'8
                g'8
                )
            }
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_fuse_09():
    """
    Tuplets must carry same multiplier.
    """

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    tuplet_2 = abjad.Tuplet((4, 5), "c'8 d'8 e'8 f'8 g'8")
    tuplets = abjad.select([tuplet_1, tuplet_2])

    with pytest.raises(Exception):
        abjad.mutate.fuse(tuplets)


def test_mutate_fuse_10():

    tuplet_1 = abjad.Tuplet((2, 3), "c'8")
    tuplet_2 = abjad.Tuplet((2, 3), "c'4")
    voice = abjad.Voice([tuplet_1, tuplet_2, abjad.Note("c'4")])
    leaves = abjad.select(voice).leaves()
    abjad.slur(leaves)

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                (
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
            }
            c'4
            )
        }
        """
    ), print(abjad.lilypond(voice))

    tuplets = voice[:2]
    abjad.mutate.fuse(tuplets)

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            \times 2/3 {
                c'8
                (
                c'4
            }
            c'4
            )
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate_fuse_11():
    """
    Fusing empty selection returns none.
    """

    staff = abjad.Staff()
    result = abjad.mutate.fuse(staff[:])
    assert result == abjad.Selection()
