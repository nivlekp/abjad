# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False to test views
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__ScorePackageWrangler_views__.py',
    )


def test_ScorePackageWrangler_clear_view_01():
    r'''Applies view and then clears view.

    Makes sure only one score is visible when view is applied.
    
    Then makes sure multiple scores are visible once view is cleared.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'vnew _test rm all'
        input_ += ' add Red~Example~Score~(2013) done <return>'
        input_ += ' vs _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - scores [_test]',
            '',
            '   1: Red Example Score (2013)',
            '',
            '      scores - copy (cp)',
            '      scores - new (new)',
            '      scores - remove (rm)',
            '      scores - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)