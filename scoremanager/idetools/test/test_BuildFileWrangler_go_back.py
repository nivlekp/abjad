# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_back_01():

    input_ = 'red~example~score u b q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013)',
        ]
    assert ide._transcript.titles == titles


def test_BuildFileWrangler_go_back_02():

    input_ = 'U b q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles