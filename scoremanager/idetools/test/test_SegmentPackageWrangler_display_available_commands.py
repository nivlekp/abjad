# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_display_available_commands_01():
    
    input_ = 'red~example~score g ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'segments - available commands' in contents


def test_SegmentPackageWrangler_display_available_commands_02():
    
    input_ = 'G ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Abjad IDE - segments - available commands' in contents