# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageWrangler_update_every_asset_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._is_repository_test = True
    input_ = 'rup* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_update