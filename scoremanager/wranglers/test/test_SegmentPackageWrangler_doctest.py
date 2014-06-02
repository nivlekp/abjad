# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_doctest_01():
    r'''In library.
    '''

    input_ = 'g pyd q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        'testable assets found ...',
        'tests passed in',
        ]
    for string in strings:
        assert string in contents

    
def test_SegmentPackageWrangler_doctest_02():
    r'''In score package.
    '''

    input_ = 'red~example~score g pyd q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        '15 testable assets found ...',
        '0 of 0 tests passed in 15 modules.',
        ]
    for string in strings:
        assert string in contents