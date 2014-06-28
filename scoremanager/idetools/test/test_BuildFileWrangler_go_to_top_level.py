# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_top_level_01():
    r'''From score build files to library.
    '''

    input_ = 'red~example~score u ** q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Abjad IDE',
        ]
    assert ide._transcript.titles == titles


def test_BuildFileWrangler_go_to_top_level_02():
    r'''From all build files to library.
    '''

    input_ = 'U ** q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        'Abjad IDE',
        ]
    assert ide._transcript.titles == titles