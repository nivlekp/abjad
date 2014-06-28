# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_doctest_01():
    r'''Works in library.
    '''

    input_ = 'M pyd q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    strings = [
        'Running doctest ...',
        'testable assets found ...',
        'tests passed in',
        ]
    for string in strings:
        assert string in contents

    
def test_MaterialPackageWrangler_doctest_02():
    r'''Works in score.
    '''

    input_ = 'red~example~score m pyd q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    strings = [
        'Running doctest ...',
        '28 testable assets found ...',
        '0 of 0 tests passed in 28 modules.',
        ]
    for string in strings:
        assert string in contents