# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class LilyPondFile(AbjadObject):
    r'''A LilyPond file.

    ..  container:: example

        **Example 1.** Makes LilyPond file:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(
            ...     music=staff,
            ...     default_paper_size=('a5', 'portrait'),
            ...     global_staff_size=16,
            ...     )

        ::

            >>> comment = 'File construct as an example.'
            >>> lilypond_file.file_initial_user_comments.append(comment)
            >>> comment = 'Parts shown here for positioning.'
            >>> lilypond_file.file_initial_user_comments.append(comment)
            >>> file_name = 'external-settings-file-1.ly'
            >>> lilypond_file.file_initial_user_includes.append(file_name)
            >>> file_name = 'external-settings-file-2.ly'
            >>> lilypond_file.file_initial_user_includes.append(file_name)
            >>> lilypond_file.header_block.composer = Markup('Josquin')
            >>> lilypond_file.header_block.title = Markup('Missa sexti tonus')
            >>> lilypond_file.layout_block.indent = 0
            >>> lilypond_file.layout_block.left_margin = 15

        ::

            >>> lilypond_file
            <LilyPondFile(4, date_time_token=DateTimeToken(date_string='...'), default_paper_size=('a5', 'portrait'), global_staff_size=16)>

        ::

            >>> print(format(lilypond_file)) # doctest: +SKIP
            % 2004-01-14 17:29

            % File construct as an example.
            % Parts shown here for positioning.

            \version "2.19.0"
            \language "english"

            \include "external-settings-file-1.ly"
            \include "external-settings-file-2.ly"

            #(set-default-paper-size "a5" 'portrait)
            #(set-global-staff-size 16)

            \header {
                composer = \markup { Josquin }
                title = \markup { Missa sexti tonus }
            }

            \layout {
                indent = #0
                left-margin = #15
            }

            \paper {
            }

            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }

        ::

            >>> show(lilypond_file) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_date_time_token',
        '_default_paper_size',
        '_file_initial_system_includes',
        '_file_initial_user_comments',
        '_file_initial_user_includes',
        '_global_staff_size',
        '_items',
        '_use_relative_includes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        date_time_token=None,
        default_paper_size=None,
        global_staff_size=None,
        use_relative_includes=None,
        ):
        from abjad.tools import lilypondfiletools
        self._items = []
        self._date_time_token = None
        if not date_time_token == False:
            self._date_time_token = lilypondfiletools.DateTimeToken()
        self._file_initial_user_comments = []
        self._file_initial_system_includes = []
        token = lilypondfiletools.LilyPondVersionToken()
        self._file_initial_system_includes.append(token)
        token = lilypondfiletools.LilyPondLanguageToken()
        self._file_initial_system_includes.append(token)
        self._file_initial_user_includes = []
        self._default_paper_size = default_paper_size
        self._global_staff_size = global_staff_size
        self._use_relative_includes = use_relative_includes

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond file.

        ..  container:: example

            **Example 1.** Gets format:

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> print(format(lilypond_file)) # doctest: +SKIP
                % 2016-01-31 20:29
                <BLANKLINE>
                \version "2.19.35"
                \language "english"
                <BLANKLINE>
                \header {}
                <BLANKLINE>
                \layout {}
                <BLANKLINE>
                \paper {}

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getitem__(self, name):
        r'''Gets LilyPond file item with `name`.

        ..  container:: example

            **Example 1.** Gets header block:

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file['header']
                <Block(name='header')>

        Raises key error when no item with `name` is found.
        '''
        for item in self.items:
            if getattr(item, 'name', None) == name:
                return item
        raise KeyError

    def __illustrate__(self):
        r'''Illustrates LilyPond file.

        Returns LilyPond file unchanged.
        '''
        return self

    def __repr__(self):
        r'''Gets interpreter representation of LilyPond file.

        ..  container:: example

            **Example 1.** Gets interpreter representation:

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file
                <LilyPondFile(4, date_time_token=DateTimeToken(date_string='...'))>

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        result = []
        if self.date_time_token is not None:
            string = '% {}'.format(self.date_time_token)
            result.append(string)
        result.extend(self._formatted_file_initial_user_comments)
        result.extend(self._formatted_file_initial_system_includes)
        if self.use_relative_includes:
            string = "#(ly:set-option 'relative-includes #t)"
            result.append(string)
        result.extend(self._formatted_file_initial_user_includes)
        result.extend(self._formatted_file_initial_scheme_settings)
        result.extend(self._formatted_blocks)
        return result

    @property
    def _formatted_blocks(self):
        result = []
        for x in self.items:
            if '_lilypond_format' in dir(x) and not isinstance(x, str):
                lilypond_format = format(x)
                if lilypond_format:
                    result.append(lilypond_format)
            else:
                result.append(str(x))
        return result

    @property
    def _formatted_file_initial_scheme_settings(self):
        result = []
        default_paper_size = self.default_paper_size
        if default_paper_size is not None:
            dimension, orientation = default_paper_size
            string = "#(set-default-paper-size \"{}\" '{})"
            string = string.format(dimension, orientation)
            result.append(string)
        global_staff_size = self.global_staff_size
        if global_staff_size is not None:
            string = '#(set-global-staff-size {})'
            string = string.format(global_staff_size)
            result.append(string)
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_system_includes(self):
        result = []
        for file_initial_include in self.file_initial_system_includes:
            if isinstance(file_initial_include, str):
                string = r'\include "{}"'.format(file_initial_include)
                result.append(string)
            else:
                result.append(format(file_initial_include))
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_user_comments(self):
        result = []
        for comment in self.file_initial_user_comments:
            if '_lilypond_format' in dir(comment) and \
                not isinstance(comment, str):
                lilypond_format = format(comment)
                if lilypond_format:
                    string = '% {}'.format(comment)
                    result.append(string)
            else:
                string = '% {!s}'.format(comment)
                result.append(string)
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _formatted_file_initial_user_includes(self):
        result = []
        for file_initial_include in self.file_initial_user_includes:
            if isinstance(file_initial_include, str):
                string = r'\include "{}"'.format(file_initial_include)
                result.append(string)
            else:
                result.append(format(file_initial_include))
        if result:
            result = ['\n'.join(result)]
        return result

    @property
    def _lilypond_format(self):
        return '\n\n'.join(self._format_pieces)

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = []
        if self.items:
            positional_argument_values.append(len(self.items))
        positional_argument_values = tuple(positional_argument_values)
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketed=True,
            is_indented=False,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def date_time_token(self):
        r'''Gets date-time token.

        ..  container:: example

            **Example 1.** Gets date-time token:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.date_time_token
                DateTimeToken()

        Returns date-time token or none.
        '''
        return self._date_time_token

    @property
    def default_paper_size(self):
        r'''Gets default paper size of LilyPond file.

        ..  container:: example

            **Example 1.** Gets default paper size:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.default_paper_size is None
                True

        Set to pair or none.

        Defaults to none.

        Returns pair or none.
        '''
        return self._default_paper_size

    @default_paper_size.setter
    def default_paper_size(self, args):
        assert args is None or len(args) == 2
        self._default_paper_size = args

    @property
    def file_initial_system_includes(self):
        r'''Gets file-initial system include commands of LilyPond file.

        ..  container:: example

            **Example 1.** Gets file-initial system includes:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.file_initial_system_includes
                [LilyPondVersionToken('...'), LilyPondLanguageToken()]

        Returns list.
        '''
        return self._file_initial_system_includes

    @property
    def file_initial_user_comments(self):
        r'''Gets file-initial user comments of Lilypond file.

        ..  container:: example

            **Example 1.** Gets file-initial user comments:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.file_initial_user_comments
                []

        Returns list.
        '''
        return self._file_initial_user_comments

    @property
    def file_initial_user_includes(self):
        r'''Gets file-initial user include commands of LilyPond file.

        ..  container:: example 

            **Example 1.** Gets file-initial user includes:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.file_initial_user_includes
                []

        Returns list.
        '''
        return self._file_initial_user_includes

    @property
    def global_staff_size(self):
        r'''Gets global staff size of LilyPond file.

        ..  container:: example

            **Example 1.** Gets global staff size:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.global_staff_size is None
                True

        Set to number or none.

        Defaults to none.

        Returns number or none.
        '''
        return self._global_staff_size

    @global_staff_size.setter
    def global_staff_size(self, arg):
        assert isinstance(arg, (int, float, int, type(None)))
        self._global_staff_size = arg

    @property
    def header_block(self):
        r'''Gets header block.

        ..  container:: example

            **Example 1.** Gets header block:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.header_block
                <Block(name='header')>

        Returns block or none.
        '''
        from abjad.tools import lilypondfiletools
        for item in self.items:
            if isinstance(item, lilypondfiletools.Block):
                if item.name == 'header':
                    return item

    @property
    def items(self):
        r'''Gets items in LilyPond file.

        ..  container:: example

            **Example 1.** Gets items:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> for item in lilypond_file.items:
                ...     item
                ...
                <Block(name='header')>
                <Block(name='layout')>
                <Block(name='paper')>
                <Block(name='score')>

        Returns list.
        '''
        return self._items

    @property
    def layout_block(self):
        r'''Gets layout block.

        ..  container:: example

            **Example 1.** Gets layout block:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.layout_block
                <Block(name='layout')>

        Returns block or none.
        '''
        from abjad.tools import lilypondfiletools
        for item in self.items:
            if isinstance(item, lilypondfiletools.Block):
                if item.name == 'layout':
                    return item

    @property
    def lilypond_language_token(self):
        r'''Gets LilyPond language token.

        ..  container:: example

            **Example 1.** Gets LilyPond language token:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.lilypond_language_token
                LilyPondLanguageToken()

        Returns LilyPond language token or none.
        '''
        from abjad.tools import lilypondfiletools
        for item in self.file_initial_system_includes:
            if isinstance(item, lilypondfiletools.LilyPondLanguageToken):
                return item

    @property
    def lilypond_version_token(self):
        r'''Gets LilyPond version token.

        ..  container:: example

            **Example 1.** Gets LilyPond version token:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.lilypond_version_token # doctest: +SKIP
                LilyPondVersionToken('2.19.35')

        Returns LilyPond version token or none.
        '''
        from abjad.tools import lilypondfiletools
        for item in self.file_initial_system_includes:
            if isinstance(item, lilypondfiletools.LilyPondVersionToken):
                return item

    @property
    def paper_block(self):
        r'''Gets paper block.

        ..  container:: example

            **Example 1.** Gets paper block:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.paper_block
                <Block(name='paper')>

        Returns block or none.
        '''
        from abjad.tools import lilypondfiletools
        for item in self.items:
            if isinstance(item, lilypondfiletools.Block):
                if item.name == 'paper':
                    return item

    @property
    def score_block(self):
        r'''Gets score block.

        ..  container:: example

            **Example 1.** Gets score block:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.score_block
                <Block(name='score')>

        Returns block or none.
        '''
        from abjad.tools import lilypondfiletools
        for item in self.items:
            if isinstance(item, lilypondfiletools.Block):
                if item.name == 'score':
                    return item

    @property
    def use_relative_includes(self):
        r'''Is true when LilyPond file should use relative includes.

        ..  container:: example

            **Example 1.** Gets relative include flag:

            ::

                >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file()

            ::

                >>> lilypond_file.use_relative_includes is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._use_relative_includes