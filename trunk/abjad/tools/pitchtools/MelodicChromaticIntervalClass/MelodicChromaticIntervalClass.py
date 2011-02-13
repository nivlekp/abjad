from fractions import Fraction
from abjad.tools import mathtools
from abjad.tools.pitchtools._ChromaticIntervalClass import _ChromaticIntervalClass
from abjad.tools.pitchtools._Interval import _Interval
from abjad.tools.pitchtools._IntervalClass import _IntervalClass
from abjad.tools.pitchtools._MelodicIntervalClass import _MelodicIntervalClass


class MelodicChromaticIntervalClass(_ChromaticIntervalClass, _MelodicIntervalClass):
   '''.. versionadded:: 1.1.2

   Abjad model of melodic chromatic interval class::

      abjad> pitchtools.MelodicChromaticIntervalClass(-14)
      MelodicChromaticIntervalClass(-2)

   Melodic chromatic interval classes are immutable.
   '''

   def __init__(self, token):
      if isinstance(token, (int, float, long, Fraction)):
         sign = mathtools.sign(token)
         abs_token = abs(token)
         if abs_token % 12 == 0 and 12 <= abs_token:
            number = 12
         else:
            number = abs_token % 12
         number *= sign
      elif isinstance(token, _Interval):
         number = token.semitones
         sign = mathtools.sign(number)
         abs_number = abs(number)
         if abs_number % 12 == 0 and 12 <= abs_number:
            number = 12
         else:
            number = abs_number % 12
         number *= sign
      elif isinstance(token, _IntervalClass):
         number = token.number
         sign = mathtools.sign(number)
         abs_number = abs(number)
         if abs_number % 12 == 0 and 12 <= abs_number:
            number = 12
         else:
            number = abs_number % 12
         number *= sign
      else:
         raise ValueError('must be number, interval or interval class.')
      object.__setattr__(self, '_number', number)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, MelodicChromaticIntervalClass):
         if self.number == arg.number:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg
