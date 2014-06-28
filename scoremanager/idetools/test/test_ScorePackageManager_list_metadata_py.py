# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
metadata_py_path = os.path.join(
    ide._configuration.example_score_packages_directory,
    'red_example_score',
    '__metadata__.py',
    )


def test_ScorePackageManager_list_metadata_py_01():

    input_ = 'red~example~score mdls q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert metadata_py_path in contents