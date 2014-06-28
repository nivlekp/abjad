# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_interpret_back_cover_01():
    r'''Works when back cover already exists.
    '''

    source_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'back-cover.tex',
        )
    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'back-cover.pdf',
        )

    with systemtools.FilesystemState(keep=[source_path, path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score u bci q'
        ide._run(input_=input_)
        assert os.path.isfile(path)
        #assert diff-pdf(path, backup_path)