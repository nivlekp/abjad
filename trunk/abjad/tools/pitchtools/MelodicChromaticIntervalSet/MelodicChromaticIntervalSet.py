from abjad.tools.pitchtools._IntervalSet import _IntervalSet
from abjad.tools.pitchtools.HarmonicChromaticIntervalSet import HarmonicChromaticIntervalSet
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval


class MelodicChromaticIntervalSet(_IntervalSet):
   '''.. versionadded:: 1.1.2

   Abjad model of melodic chromatic interval set::

      abjad> pitchtools.MelodicChromaticIntervalSet([11, 11, 13.5, 13.5])
      MelodicChromaticIntervalSet(+11, +13.5)

   Melodic chromatic interval sets are immutable.
   '''

   def __new__(self, interval_tokens):
      mcis = [MelodicChromaticInterval(x) for x in interval_tokens]
      return frozenset.__new__(self, mcis)

   ## OVERLOADS ##

   def __copy__(self):
      return MelodicChromaticIntervalSet(self)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      intervals = list(self.intervals)
      intervals.sort(lambda x, y: cmp(x.number, y.number))
      return ', '.join([str(x) for x in intervals])

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
