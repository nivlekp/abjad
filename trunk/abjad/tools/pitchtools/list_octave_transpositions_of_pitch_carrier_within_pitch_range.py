from abjad.components import Chord
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.PitchRange import PitchRange
from abjad.tools.pitchtools.NamedChromaticPitchSet import NamedChromaticPitchSet
from abjad.tools.pitchtools.transpose_pitch_carrier_by_melodic_chromatic_interval import \
   transpose_pitch_carrier_by_melodic_chromatic_interval


## TODO: Reimplement pitchtools.list_octave_transpositions_of_pitch_carrier_within_pitch_range( ) to work on Abjad PitchSet, Note and Chord objects only. ##

## TODO: Reimplement pitchtools.octave_transposition( ) with diatonic transposition. ##

## FIXME: currently broken now that chords correctly copy tweaked noteheads;
##        make this function work with tweaked chords
def list_octave_transpositions_of_pitch_carrier_within_pitch_range(pitches, pitch_range):
   r"""List octave transpositions of `pitches` in `pitch_range`.

   ::
      
      abjad> chord = Chord([0, 2, 4], (1, 4))
      abjad> pitch_range = pitchtools.PitchRange(0, 48)
      abjad> pitchtools.list_octave_transpositions_of_pitch_carrier_within_pitch_range(chord, pitch_range)
      [Chord(c' d' e', 4), Chord(c'' d'' e'', 4), Chord(c''' d''' e''', 4), Chord(c'''' d'''' e'''', 4)]
   """

   if not isinstance(pitch_range, PitchRange):
      raise TypeError('must be pitch range.')

   if all([isinstance(x, (int, long, float)) for x in pitches]):
      return _pitch_number_list_octave_transpositions(pitches, pitch_range)

   if not isinstance(pitches, (Chord, NamedChromaticPitchSet)):
      raise TypeError('must be pitches or pitch set.')

   result = [ ]

   interval = MelodicChromaticInterval(-12)
   while True:
      candidate = transpose_pitch_carrier_by_melodic_chromatic_interval(pitches, interval)
      if candidate in pitch_range:
         result.append(candidate)
         interval -= MelodicChromaticInterval(12) 
      else:
         break

   result.reverse( )

   interval = MelodicChromaticInterval(0)
   while True:
      candidate = transpose_pitch_carrier_by_melodic_chromatic_interval(pitches, interval)
      if candidate in pitch_range:
         result.append(candidate)
         interval += MelodicChromaticInterval(12) 
      else:
         break

   return result


def _pitch_number_list_octave_transpositions(pitch_number_list, pitch_range):
   result = [ ]
   ps = set(pitch_number_list)
   start_pitch_number = abs(pitch_range._start_pitch.numbered_chromatic_pitch)
   stop_pitch_number = abs(pitch_range._stop_pitch.numbered_chromatic_pitch)
   R = set(range(start_pitch_number, stop_pitch_number + 1))
   while ps.issubset(R):
      next = list(ps)
      next.sort( )
      result.extend([next])
      ps = set([p + 12 for p in ps])

   ps = set([p - 12 for p in pitch_number_list])
   while ps.issubset(R):
      next = list(ps)
      next.sort( )
      result.extend([next])
      ps = set([p - 12 for p in ps])

   result.sort( )
   return result
