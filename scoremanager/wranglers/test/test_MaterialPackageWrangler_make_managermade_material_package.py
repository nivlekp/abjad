# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_managermade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testsargasso'
    assert not wrangler._configuration.package_exists(string)
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )

    try:
        command = 'sargasso testsargasso q'
        wrangler.make_managermade_material_package(pending_user_input=command)
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)


def test_MaterialPackageWrangler_make_managermade_material_package_02():
    r'''Menu title is correct.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm nmm q')

    transcript = score_manager._transcript
    string = 'Select material manager:'
    assert transcript.last_title == string
