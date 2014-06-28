# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_invoke_python_01():
    
    input_ = 'red~example~score g pyi 2**38 q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert '274877906944' in contents


def test_SegmentPackageWrangler_invoke_python_02():
    
    input_ = 'G pyi 2**38 q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert '274877906944' in contents