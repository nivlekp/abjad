# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False to test views
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__MaterialPackageWrangler_views__.py',
    )


def test_MaterialPackageWrangler_clear_view_01():
    r'''Works in library.
    
    Applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'm vnew _test rm all'
        input_ += ' add instrumentation~(Red~Example~Score) done <return>'
        input_ += ' vs _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Abjad IDE - materials [_test]',
            '',
            '   1: instrumentation (Red Example Score)',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines for _ in transcript)


def test_MaterialPackageWrangler_clear_view_02():
    r'''Works in score.

    Applies view and then clears view.

    Makes sure only one material package is visible when view is applied.
    
    Then makes sure multiple material packages are visible once view is 
    cleared.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'red~example~score m vnew _test rm all'
        input_ += ' add instrumentation done <return>'
        input_ += ' vs _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Red Example Score (2013) - materials [_test]',
            '',
            '   1: instrumentation',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines for _ in transcript)