from abjad import *


def test_pitchtools_PC___sub___01( ):

   pc1 = pitchtools.PC(6)
   pc2 = pitchtools.PC(7)

   assert pc1 - pc2 == pitchtools.PC(11)
   assert pc2 - pc1 == pitchtools.PC(1)
