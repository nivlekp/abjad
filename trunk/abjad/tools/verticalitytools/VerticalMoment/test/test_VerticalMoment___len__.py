from abjad import *


def test_VerticalMoment___len___01( ):

   score = Score([ ])
   score.append(Staff([tuplettools.FixedDurationTuplet((4, 8), notetools.make_repeated_notes(3))]))
   piano_staff = scoretools.PianoStaff([ ])
   piano_staff.append(Staff(notetools.make_repeated_notes(2, Rational(1, 4))))
   piano_staff.append(Staff(notetools.make_repeated_notes(4)))
   marktools.ClefMark('bass')(piano_staff[1])
   score.append(piano_staff)
   macros.diatonicize(list(reversed(score.leaves)))

   r'''
   \new Score <<
           \new Staff {
                   \times 4/3 {
                           d''8
                           c''8
                           b'8
                   }
           }
           \new PianoStaff <<
                   \new Staff {
                           a'4
                           g'4
                   }
                   \new Staff {
                           \clef "bass"
                           f'8
                           e'8
                           d'8
                           c'8
                   }
           >>
   >>
   '''

   vertical_moment = verticalitytools.get_vertical_moment_at_prolated_offset_in_expr(
      score, Rational(1, 8))
   "VerticalMoment(Score<<2>>, Staff{1}, {@ 3:4 d''8, c''8, b'8 @}, d''8, PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"
   assert len(vertical_moment) == 9

   vertical_moment = verticalitytools.get_vertical_moment_at_prolated_offset_in_expr(
      score[0], Rational(1, 8))
   "VerticalMoment(Staff{1}, {@ 3:4 d''8, c''8, b'8 @}, d''8)"
   assert len(vertical_moment) == 3

   vertical_moment = verticalitytools.get_vertical_moment_at_prolated_offset_in_expr(
      piano_staff, Rational(1, 8))
   "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"
   assert len(vertical_moment) == 5

   vertical_moment = verticalitytools.get_vertical_moment_at_prolated_offset_in_expr(
      piano_staff[0], Rational(1, 8))
   "VerticalMoment(Staff{2}, a'4)"
   assert len(vertical_moment) == 2

   vertical_moment = verticalitytools.get_vertical_moment_at_prolated_offset_in_expr(
      piano_staff[1], Rational(1, 8))
   "VerticalMoment(Staff{2}, e'8)"
   assert len(vertical_moment) == 2
