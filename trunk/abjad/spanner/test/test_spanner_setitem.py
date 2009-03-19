from abjad import *


def test_spanner_setitem_01( ):
   '''Extend spanner at left.'''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[1])

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }'''

   p[0:0] = [t[0]]

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }'''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
   assert check(t)


def test_spanner_setitem_02( ):
   '''Reset all spanner contents.'''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[1])

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }'''

   p[ : ] = t[ : ]

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
   assert check(t)


def test_spanner_setitem_03( ):
   '''Set a single positive integer index in spanner.'''

   t = Voice(scale(4))
   p = Beam(t[:])

   p[1] = Note(14, (1, 8))

   r'''\new Voice {
      c'8 [
      d''8
      e'8
      f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td''8\n\te'8\n\tf'8 ]\n}"


def test_spanner_setitem_04( ):
   '''Set a single negative integer index in spanner.'''

   t = Voice(scale(4))
   p = Beam(t[:])

   p[-1] = Note(17, (1, 8))

   r'''\new Voice {
      c'8 [
      d''8
      e'8
      f''8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf''8 ]\n}"
