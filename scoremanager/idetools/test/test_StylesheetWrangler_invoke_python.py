# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_invoke_python_01():
    
    input_ = 'red~example~score y pyi 2**38 q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert '274877906944' in contents


def test_StylesheetWrangler_invoke_python_02():
    
    input_ = 'Y pyi 2**38 q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert '274877906944' in contents