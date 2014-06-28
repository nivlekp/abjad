# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_invoke_shell_01():
    r'''Outside of score package.
    '''

    input_ = 'D !pwd q'
    ide._run(input_=input_)

    path = os.path.join(
        ide._configuration.score_manager_directory,
        )
    string = '\n{}\n'.format(path)
    assert string in ide._transcript.contents


def test_DistributionFileWrangler_invoke_shell_02():
    r'''Inside score package.
    '''

    input_ = 'red~example~score d !pwd q'
    ide._run(input_=input_)

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        )
    string = '\n{}\n'.format(path)
    assert string in ide._transcript.contents