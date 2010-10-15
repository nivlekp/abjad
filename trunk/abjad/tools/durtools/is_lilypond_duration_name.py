import re


lilypond_duration_name_regex_body = r'''
   (\\breve|\\longa|\\maxima)   ## exactly one of three duration names
   '''

lilypond_duration_name_regex = re.compile('^%s$' % 
   lilypond_duration_name_regex_body, re.VERBOSE)

def is_lilypond_duration_name(expr):
   '''True when `expr` is a LilyPond duartion name. Otherwise false::

      abjad> durtools.is_lilypond_duration_name('breve')
      True

   The regex ``^(\\breve|\\longa|\\maxima)$`` underlies this predicate.
   '''

   if not isinstance(expr, str):
      return False

   return bool(lilypond_duration_name_regex.match(expr))
