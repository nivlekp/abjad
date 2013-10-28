from abjad import *
from experimental.demos.bach.chorale import es_ist_genug


def build_chorale():

    soprano = p(r'\new Voice = "soprano" {{ {} }}'.format(es_ist_genug['soprano']))
    alto =    p(r'\new Voice = "alto" {{ {} }}'.format(es_ist_genug['alto']))
    tenor =   p(r'\new Voice = "tenor" {{ {} }}'.format(es_ist_genug['tenor']))
    bass =    p(r'\new Voice = "bass" {{ {} }}'.format(es_ist_genug['bass']))

    treble_staff = Staff([soprano, alto])
    bass_staff = Staff([tenor, bass])

    treble_staff.is_simultaneous = True
    bass_staff.is_simultaneous = True

    key_signature = contexttools.KeySignatureMark(*es_ist_genug['key'])
    attach(key_signature, treble_staff)
    key_signature = contexttools.KeySignatureMark(*es_ist_genug['key'])
    attach(key_signature, bass_staff)
    clef = contexttools.ClefMark('bass')
    attach(clef, bass_staff)

    bar_line = marktools.BarLine('|.')
    attach(bar_line, treble_staff)
    bar_line = marktools.BarLine('|.')
    attach(bar_line, bass_staff)

    piano_staff = scoretools.PianoStaff([treble_staff, bass_staff])

    return piano_staff
