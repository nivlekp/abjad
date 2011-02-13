from abjad.tools.pitchtools._IntervalSet import _IntervalSet
from abjad.tools.pitchtools.HarmonicChromaticIntervalSet import HarmonicChromaticIntervalSet
from abjad.tools.pitchtools.HarmonicDiatonicInterval import HarmonicDiatonicInterval


class HarmonicDiatonicIntervalSet(_IntervalSet):
   '''.. versionadded:: 1.1.2

   Abjad model of harmonic diatonic interval set::

      abjad> pitchtools.HarmonicDiatonicIntervalSet('m2 m2 M2 M9')
      HarmonicDiatonicIntervalSet('m2 M2 M9')

   Harmonic diatonic interval sets are immutable.
   '''

   def __new__(self, arg):
      if isinstance(arg, str):
         interval_tokens = arg.split( )
      else:
         interval_tokens = arg
      hdis = [HarmonicDiatonicInterval(x) for x in interval_tokens]
      return frozenset.__new__(self, hdis)

   ## OVERLOADS ##

   def __copy__(self):
      return HarmonicDiatonicIntervalSet(self)

   def __repr__(self):
      return "%s('%s')" % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ' '.join([str(x) for x in sorted(self.intervals)])

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_set(self):
      return HarmonicChromaticIntervalSet(self)

   @property
   def intervals(self):
      return set(self)
      
   @property
   def numbers(self):
      return set([interval.number for interval in self])
