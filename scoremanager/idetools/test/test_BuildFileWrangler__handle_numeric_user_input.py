# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler__handle_numeric_user_input_01():

    input_ = 'red~example~score u 1 q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file