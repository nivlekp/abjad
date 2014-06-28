# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_doctest_01():
    r'''In library.
    '''

    input_ = 'Y pyd q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    strings = [
        'Running doctest ...',
        'No testable assets found.',
        ]
    for string in strings:
        assert string in contents

    
def test_StylesheetWrangler_doctest_02():
    r'''In score package.
    '''

    input_ = 'red~example~score y pyd q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    strings = [
        'Running doctest ...',
        'No testable assets found.',
        ]
    for string in strings:
        assert string in contents