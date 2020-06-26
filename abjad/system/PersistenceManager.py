import os
import re
import shutil
import tempfile

from ..formatting import LilyPondFormatManager
from ..storage import StorageFormatManager
from .IOManager import IOManager
from .Timer import Timer


class PersistenceManager(object):
    """
    Persistence manager.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.persist(staff)
        PersistenceManager(client=Staff("c'4 e'4 d'4 f'4"))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_client",)

    _png_page_pattern = re.compile(r".+page(\d+)\.png")

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Client of persistence manager.

        Returns component or selection.
        """
        return self._client

    ### PUBLIC METHODS ###

    def as_ly(
        self, ly_file_path, *, illustrate_function=None, strict=None, **keywords,
    ):
        """
        Persists client as LilyPond file.

        Returns output path and elapsed formatting time when LilyPond output is
        written.
        """
        if strict is not None:
            assert isinstance(strict, int), repr(strict)
        if illustrate_function is None:
            assert hasattr(self._client, "__illustrate__")
            illustrate_function = self._client.__illustrate__
        lilypond_file = illustrate_function(**keywords)
        assert ly_file_path is not None, repr(ly_file_path)
        ly_file_path = str(ly_file_path)
        ly_file_path = os.path.expanduser(ly_file_path)
        assert ly_file_path.endswith(".ly"), ly_file_path
        timer = Timer()
        with timer:
            string = lilypond_file.__format__(format_specification="lilypond")
            if isinstance(strict, int):
                string = LilyPondFormatManager.align_tags(string, strict)
        abjad_formatting_time = timer.elapsed_time
        directory = os.path.dirname(ly_file_path)
        IOManager._ensure_directory_existence(directory)
        with open(ly_file_path, "w") as file_pointer:
            file_pointer.write(string)
        return ly_file_path, abjad_formatting_time

    def as_midi(self, midi_file_path, *, remove_ly=False, **keywords):
        """
        Persists client as MIDI file.

        Returns 4-tuple of output MIDI path, Abjad formatting time, LilyPond
        rendering time and success boolean.
        """
        if hasattr(self._client, "score_block"):
            lilypond_file = self._client
        else:
            assert hasattr(self._client, "__illustrate__")
            lilypond_file = self._client.__illustrate__(**keywords)
        assert hasattr(lilypond_file, "score_block")
        if midi_file_path is not None:
            midi_file_path = os.path.expanduser(midi_file_path)
            without_extension = os.path.splitext(midi_file_path)[0]
            ly_file_path = f"{without_extension}.ly"
        else:
            ly_file_path = None
        result = type(self)(lilypond_file).as_ly(ly_file_path, **keywords)
        ly_file_path, abjad_formatting_time = result
        timer = Timer()
        with timer:
            success = IOManager.run_lilypond(ly_file_path)
        lilypond_rendering_time = timer.elapsed_time
        if remove_ly:
            os.remove(ly_file_path)
        if os.name == "nt":
            extension = "mid"
        else:
            extension = "midi"
        path = os.path.splitext(ly_file_path)[0]
        midi_file_path = f"{path}.{extension}"
        return (
            midi_file_path,
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )

    def as_pdf(
        self,
        pdf_file_path,
        *,
        illustrate_function=None,
        remove_ly=False,
        strict=None,
        **keywords,
    ):
        """
        Persists client as PDF.

        Returns output path, elapsed formatting time and elapsed rendering
        time when PDF output is written.
        """
        if strict is not None:
            assert isinstance(strict, int), repr(strict)
        if illustrate_function is None:
            assert hasattr(self._client, "__illustrate__"), repr(self._client)
        if pdf_file_path is not None:
            pdf_file_path = str(pdf_file_path)
            pdf_file_path = os.path.expanduser(pdf_file_path)
            without_extension = os.path.splitext(pdf_file_path)[0]
            ly_file_path = "{}.ly".format(without_extension)
        else:
            ly_file_path = None
        result = self.as_ly(
            ly_file_path,
            illustrate_function=illustrate_function,
            strict=strict,
            **keywords,
        )
        ly_file_path, abjad_formatting_time = result
        without_extension = os.path.splitext(ly_file_path)[0]
        pdf_file_path = "{}.pdf".format(without_extension)
        timer = Timer()
        with timer:
            success = IOManager.run_lilypond(ly_file_path)
        lilypond_rendering_time = timer.elapsed_time
        if remove_ly:
            os.remove(ly_file_path)
        return (
            pdf_file_path,
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )

    def as_png(
        self,
        png_file_path,
        *,
        flags="--png",
        illustrate_function=None,
        preview=False,
        remove_ly=False,
        resolution=False,
        **keywords,
    ):
        """
        Persists client as PNG.

        Autogenerates file path when ``png_file_path`` is none.

        Returns output path(s), elapsed formatting time and elapsed rendering
        time.
        """
        if illustrate_function is None:
            assert hasattr(self._client, "__illustrate__")
        if png_file_path is not None:
            png_file_path = os.path.expanduser(png_file_path)
            without_extension = os.path.splitext(png_file_path)[0]
            ly_file_path = "{}.ly".format(without_extension)
        else:
            ly_file_path = None
        result = self.as_ly(
            ly_file_path, illustrate_function=illustrate_function, **keywords
        )

        ly_file_path, abjad_formatting_time = result

        original_directory = os.path.split(ly_file_path)[0]
        original_ly_file_path = ly_file_path
        temporary_directory = tempfile.mkdtemp()
        temporary_ly_file_path = os.path.join(
            temporary_directory, os.path.split(ly_file_path)[1]
        )
        shutil.copy(original_ly_file_path, temporary_ly_file_path)

        # render lilypond flags
        if preview:
            flags = "-dpreview"
        if resolution and isinstance(resolution, int):
            flags += " -dresolution={}".format(resolution)

        timer = Timer()
        with timer:
            success = IOManager.run_lilypond(temporary_ly_file_path, flags=flags)
        lilypond_rendering_time = timer.elapsed_time

        png_file_paths = []
        for file_name in os.listdir(temporary_directory):
            if not file_name.endswith(".png"):
                continue
            source_png_file_path = os.path.join(temporary_directory, file_name)
            target_png_file_path = os.path.join(original_directory, file_name)
            shutil.move(source_png_file_path, target_png_file_path)
            png_file_paths.append(target_png_file_path)
        shutil.rmtree(temporary_directory)

        if remove_ly:
            os.remove(ly_file_path)

        if 1 < len(png_file_paths):
            png_file_paths.sort(
                key=lambda x: int(self._png_page_pattern.match(x).groups()[0])
            )

        return (
            tuple(png_file_paths),
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )
