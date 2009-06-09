from abjad.tools.mathtools.binary_string import binary_string


def integer_decompose(n):
   '''Return big-ending tuple ``t = (t_0, ..., t_j)`` such that
   
   *  ``sum(t) == n``
   *  ``t_i`` can be written without recourse to ties, and
   *  ``t_(i + 1) < t_i`` for every ``t_i`` in ``t``.

   That is, partition positive integer *n* into strictly decreasing
   integer parts, each of which can be written without recourse to ties.

   ::

      abjad> for n in range(1, 11):
      ...     print n, mathtools.integer_decompose(n)
      ... 
      1 (1,)
      2 (2,)
      3 (3,)
      4 (4,)
      5 (4, 1)
      6 (6,)
      7 (7,)
      8 (8,)
      9 (8, 1)
      10 (8, 2)

   ::

      abjad> for n in range(11, 21):
      ...     print n, mathtools.integer_decompose(n)
      ... 
      11 (8, 3)
      12 (12,)
      13 (12, 1)
      14 (14,)
      15 (15,)
      16 (16,)
      17 (16, 1)
      18 (16, 2)
      19 (16, 3)
      20 (16, 4)

   Raise :exc:`TypeError` on noninteger *n*::

      abjad> mathtools.integer_decompose(7.5)
      TypeError

   Raise :exc:`ValueError` on nonpositive integer *n*::

      abjad> mathtools.integer_decompose(-1)
      ValueError

'''

   if not isinstance(n, (int, long)):
      raise TypeError

   if n < 0:
      raise ValueError

   if n == 0:
      return (0, )
   
   result = [ ]
   prev_empty = True
   binary_n = binary_string(n)
   binary_length = len(binary_n)

   for i, x in enumerate(binary_n):
      if x == '1':
         place_value = 2 ** (binary_length - i - 1)
         if prev_empty:
            result.append(place_value)
         else:
            result[-1] += place_value
         prev_empty = False
      else:
         prev_empty = True

   return tuple(result)
