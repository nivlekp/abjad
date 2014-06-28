# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False for view tests
ide = scoremanager.idetools.AbjadIDE(is_test=False)


def test_MaterialPackageWrangler_set_view_01():
    r'''Works in library.
    
    Makes sure only select material packages are visible.
    '''
    
    views_file = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__MaterialPackageWrangler_views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = 'M va add _test'
        input_ += ' add instrumentation~(Red~Example~Score)'
        input_ += ' add tempo~inventory~(Red~Example~Score) done done'
        input_ += ' vs _test q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Abjad IDE - materials [_test]',
            '',
            '    Red Example Score:',
            '       1: instrumentation',
            '       2: tempo inventory',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines for _ in transcript)


def test_MaterialPackageWrangler_set_view_02():
    r'''Works in score.
    
    Makes sure only select material package is visible.
    '''
    
    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = 'red~example~score m va add _test'
        input_ += ' add instrumentation done done'
        input_ += ' vs _test q'
        ide._run(input_=input_)
        transcript = ide._transcript

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
        assert any(_.lines == lines for _ in transcript)


def test_MaterialPackageWrangler_set_view_03():
    r'''Works with metadata.
    '''

    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'red~example~score m vs inventories q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Red Example Score (2013) - materials [inventories]',
            '',
            '   1: pitch range inventory',
            '   2: tempo inventory',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_MaterialPackageWrangler_set_view_04():
    r'''Works with :ds: display string token.

    The 'inventories' view is defined equal to "'inventory' in :ds:".
    '''

    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'red~example~score m vs inventories q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Red Example Score (2013) - materials [inventories]',
            '',
            '   1: pitch range inventory',
            '   2: tempo inventory',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_MaterialPackageWrangler_set_view_05():
    r'''Works with :path: display string token.

    The 'magic' view is defined equal to "'magic_' in :path:".
    '''

    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'red~example~score m vs magic q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Red Example Score (2013) - materials [magic]',
            '',
            '   1: magic numbers',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)