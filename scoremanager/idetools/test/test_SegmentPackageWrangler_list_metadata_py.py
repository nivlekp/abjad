# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_list_metadata_py_01():

    metadata_py_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        '__metadata__.py',
        )

    input_ = 'red~example~score g mdls q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert metadata_py_path in contents


def test_SegmentPackageWrangler_list_metadata_py_02():

    metadata_py_path = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__metadata__.py',
        )

    input_ = 'G mdls q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert metadata_py_path in contents