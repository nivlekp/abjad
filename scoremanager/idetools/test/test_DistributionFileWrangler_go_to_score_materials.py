# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_score_materials_01():
    r'''Goes from score distribution files to score materials.
    '''

    input_ = 'red~example~score d m q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013) - materials',
        ]
    assert ide._transcript.titles == titles