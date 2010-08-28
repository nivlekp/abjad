from abjad.tools.verticalitytools.iterate_vertical_moments_forward_in_expr import iterate_vertical_moments_forward_in_expr


def label_vertical_moments_in_expr_with_pitch_numbers(expr):
   r'''.. versionadded:: 1.1.2

   Label pitch numbers of every vertical moment in `expr`. ::

      abjad> score = Score(Staff([ ]) * 3)
      abjad> score[0].extend(macros.scale(4))
      abjad> marktools.ClefMark('alto')(score[1])
      abjad> score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
      abjad> marktools.ClefMark('bass')(score[2])
      abjad> score[2].append(Note(-24, (1, 2)))
      abjad> verticalitytools.label_vertical_moments_in_expr_with_pitch_numbers(score)
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8 _ \markup { \small { \column { 2 -5 -24 } } }
                      e'8
                      f'8 _ \markup { \small { \column { 5 -7 -24 } } }
              }
              \new Staff {
                      \clef "alto"
                      g4
                      f4 _ \markup { \small { \column { 4 -7 -24 } } }
              }
              \new Staff {
                      \clef "bass"
                      c,2 _ \markup { \small { \column { 0 -5 -24 } } }
              }
      >>

   .. versionchanged:: 1.1.2
      renamed ``label.vertical_moment_pitch_numbers( )`` to
      ``verticalitytools.label_vertical_moments_in_expr_with_pitch_numbers( )``.
   '''
   from abjad.tools import pitchtools

   for vertical_moment in iterate_vertical_moments_forward_in_expr(expr):
      leaves = vertical_moment.leaves
      pitches = pitchtools.list_named_pitches_in_expr(leaves)
      if not pitches:
         continue
      pitch_numbers = [pitch.number for pitch in pitches]
      pitch_numbers = ' '.join([str(x) for x in pitch_numbers])
      pitch_numbers = r'\small { \column { %s } }' % pitch_numbers
      vertical_moment.start_leaves[-1].markup.down.append(pitch_numbers)
