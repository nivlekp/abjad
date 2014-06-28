# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_open_views_py_01():

    input_ = 'U vo q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file


def test_BuildFileWrangler_open_views_py_02():

    input_ = 'blue~example~score u vo q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert not ide._session._attempted_to_open_file
    assert 'No __views.py__ found.' in contents