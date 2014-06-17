# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
from experimental import *
import scoremanager


def test_MaterialPackageManager_autoedit_definition_py_01():
    '''Edit menu has correct header.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'm example~markup~inventory da q'
    score_manager._run(input_=input_)

    title = 'Abjad IDE - materials - example markup inventory (Abjad)'
    assert title in score_manager._transcript.titles


def test_MaterialPackageManager_autoedit_definition_py_02():
    r'''Edits tempo inventory.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_tempo_inventory',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'versions',
        ]
    inventory = indicatortools.TempoInventory([
        ((1, 4), 60),
        ((1, 4), 90),
        ])

    assert not os.path.exists(path)

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new test~tempo~inventory y da y TempoInventory'
        input_ += ' add ((1, 4), 60) add ((1, 4), 90) done y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries


def test_MaterialPackageManager_autoedit_definition_py_03():
    r'''Edits empty pitch range inventory.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_pitch_range_inventory',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'versions',
        ]
    inventory = pitchtools.PitchRangeInventory()

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new test~pitch~range~inventory y'
        input_ += ' da y PitchRangeInventory done y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries


def test_MaterialPackageManager_autoedit_definition_py_04():
    r'''Edits populated pitch range inventory.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_pitch_range_inventory',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]
    inventory = pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, G5]'),
        pitchtools.PitchRange('[C2, F#5]'),
        ])
    input_ = 'm new test~pitch~range~inventory y'
    input_ += ' da y PitchRangeInventory'
    input_ += ' add [A0, C8]'
    input_ += ' add [C2, F#5]'
    input_ += ' add [C2, G5]'
    input_ += ' rm 1 mv 1 2 b y dp y q'

    with systemtools.FilesystemState(remove=[path]):
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory


def test_MaterialPackageManager_autoedit_definition_py_05():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_markup_inventory',
        )
    inventory = markuptools.MarkupInventory(
        [
            markuptools.Markup(
                '\\italic { serenamente }',
                ),
            markuptools.Markup(
                '\\italic { presto }',
                )
            ],
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = "m new test~markup~inventory y da y MarkupInventory"
        input_ += " add arg r'\\italic~{~serenamente~}' done"
        input_ += " add arg r'\\italic~{~presto~}' done done y dp y q"
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory


def test_MaterialPackageManager_autoedit_definition_py_06():
    r'''Edits empty octave transposition mapping inventory.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_transposition_inventory',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]
    inventory = pitchtools.OctaveTranspositionMappingInventory()

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new test~transposition~inventory y'
        input_ += ' da y OctaveTranspositionMappingInventory'
        input_ += ' done y dp y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory


def test_MaterialPackageManager_autoedit_definition_py_07():
    r'''Edits populated octave transposition mapping inventory.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_transposition_inventory',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]
    mapping_1 = pitchtools.OctaveTranspositionMapping([
        ('[A0, C4)', 15),
        ('[C4, C8)', 27),
        ])
    mapping_2 = pitchtools.OctaveTranspositionMapping([
        ('[A0, C8]', -18),
        ])
    inventory = pitchtools.OctaveTranspositionMappingInventory([
        mapping_1,
        mapping_2
        ])

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new test~transposition~inventory y'
        input_ += ' da y OctaveTranspositionMappingInventory'
        input_ += " add add ('[A0, C4)', 15)"
        input_ += " add ('[C4, C8)', 27) done"
        input_ += " add add ('[A0, C8]', -18)"
        input_ += ' done done y dp y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == inventory


def test_MaterialPackageManager_autoedit_definition_py_08():
    pytest.skip('make autoadding work again.')

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_list',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new test~list y da y list 17 foo done dp y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == [17, 'foo']


def test_MaterialPackageManager_autoedit_definition_py_09():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_list',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new test~list y da y list'
        input_ += ' add 17 add foo done y dp y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == [17, 'foo']


def test_MaterialPackageManager_autoedit_definition_py_10():
    r'''Edits talea rhythm-maker.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_rhythm_maker',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]
    talea = rhythmmakertools.Talea(
        counts=(-1, 2, -3, 4),
        denominator=16,
        )
    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        split_divisions_by_counts=(6,),
        extra_counts_per_division=(2, 3),
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new test~rhythm~maker y da y TaleaRhythmMaker'
        input_ += ' add talea counts (-1, 2, -3, 4) denominator 16 done'
        input_ += ' split (6,)'
        input_ += ' extra (2, 3)'
        input_ += ' done y dp y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == maker


def test_MaterialPackageManager_autoedit_definition_py_11():
    r'''Edits retierated articulation handler.
    '''
    pytest.skip('make me work again.')

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_articulation_handler',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]
    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_duration=Duration(1, 64),
        maximum_duration=Duration(1, 4),
        minimum_written_pitch=NamedPitch('c'),
        maximum_written_pitch=NamedPitch("c''''"),
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = "m new test~articulation~handler y"
        input_ += " da y ReiteratedArticulationHandler"
        input_ += " al ['^', '.'] nd (1, 64) xd (1, 4) np c xp c''''"
        input_ += " done y dp y q"
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == handler


def test_MaterialPackageManager_autoedit_definition_py_12():
    r'''Edits dynamic handler.
    '''
    pytest.skip('make me work again.')

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory,
        'test_dynamic_handler',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'output.py',
        'versions',
        ]
    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new test~dynamic~handler y'
        input_ += ' da y ReiteratedDynamicHandler'
        input_ += ' dy f md (1, 16) done y dp y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_py()
        assert output_material == handler


def test_MaterialPackageManager_autoedit_definition_py_13():
    r'''Target tempo inventory.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'test_tempo_inventory',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'versions',
        ]
    inventory = indicatortools.TempoInventory([
        ((1, 4), 60),
        ((1, 4), 90),
        ])

    assert not os.path.exists(path)

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score m new test~tempo~inventory y'
        input_ += ' da y TempoInventory'
        input_ += ' add ((1, 4), 60) add ((1, 4), 90) done y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        target = manager._execute_definition_py()
        assert target == inventory


def test_MaterialPackageManager_autoedit_definition_py_14():
    r'''Skips rewrite when target has not changed.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score instrumentation da done q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Will write' not in contents