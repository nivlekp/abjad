from abjad import *


def test_label_vertical_moment_interval_class_vectors_01( ):

   score = Score(Staff([ ]) * 3)
   score[0].extend(construct.scale(4))
   score[1].clef.forced = Clef('alto')
   score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
   score[2].clef.forced = Clef('bass')
   score[2].append(Note(-24, (1, 2)))
   label.vertical_moment_interval_class_vectors(score)

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8 _ \markup { \tiny { 0010020 } }
                   e'8
                   f'8 _ \markup { \tiny { 1000020 } }
           }
           \new Staff {
                   \clef "alto"
                   g4
                   f4 _ \markup { \tiny { 0100110 } }
           }
           \new Staff {
                   \clef "bass"
                   c,2 _ \markup { \tiny { 1000020 } }
           }
   >>
   '''

   assert check.wf(score)
   assert score.format == '\\new Score <<\n\t\\new Staff {\n\t\tc\'8\n\t\td\'8 _ \\markup { \\tiny { 0010020 } }\n\t\te\'8\n\t\tf\'8 _ \\markup { \\tiny { 1000020 } }\n\t}\n\t\\new Staff {\n\t\t\\clef "alto"\n\t\tg4\n\t\tf4 _ \\markup { \\tiny { 0100110 } }\n\t}\n\t\\new Staff {\n\t\t\\clef "bass"\n\t\tc,2 _ \\markup { \\tiny { 1000020 } }\n\t}\n>>'


def test_label_vertical_moment_interval_class_vectors_02( ):
   '''Vertical moments with quartertones format with a two-row
   interval class vector. Top for 12-ET, bottom for 24-ET.'''

   chord = Chord([-2, -1.5, 9], (1, 4))
   label.vertical_moment_interval_class_vectors(chord)

   r'''
   <bf bqf a'>4 _ \markup { \tiny { \column { "0100000" "110000" } } }
   '''

   assert chord.format == '<bf bqf a\'>4 _ \\markup { \\tiny { \\column { "0100000" "110000" } } }'
