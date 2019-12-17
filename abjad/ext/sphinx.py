import copy
import enum
import hashlib
import os
import pathlib
import subprocess
import typing

from docutils.nodes import (
    Element,
    FixedTextElement,
    General,
    SkipNode,
    image,
    literal_block,
)
from docutils.parsers.rst import Directive, directives
from sphinx.util import FilenameUniqDict, logging
from sphinx.util.nodes import set_source_info
from uqbar.book.extensions import Extension
from uqbar.strings import normalize

from abjad import abjad_configuration
from abjad.iox import Illustrator, LilyPondIO, Player
from abjad.lilypondfile import Block, LilyPondVersionToken
from abjad.system import TemporaryDirectoryChange

logger = logging.getLogger(__name__)


class HiddenDoctestDirective(Directive):
    """
    An hidden doctest directive.

    Contributes no formatting to documents built by Sphinx.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: typing.Dict[str, str] = {}

    ### PUBLIC METHODS ###

    def run(self):
        """Executes the directive.
        """
        self.assert_has_content()
        return []


class ShellDirective(Directive):
    """
    An shell directive.

    Represents a shell session.

    Generates a docutils ``literal_block`` node.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: typing.Dict[str, str] = {}

    ### PUBLIC METHODS ###

    def run(self):
        self.assert_has_content()
        result = []
        with TemporaryDirectoryChange(abjad_configuration.abjad_directory):
            cwd = pathlib.Path.cwd()
            for line in self.content:
                result.append(f"{cwd.name}$ {line}")
                completed_process = subprocess.run(
                    line,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                result.append(completed_process.stdout)
        code = "\n".join(result)
        literal = literal_block(code, code)
        literal["language"] = "console"
        set_source_info(self, literal)
        return [literal]


class ThumbnailDirective(Directive):
    """
    A thumbnail directive.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    final_argument_whitespace = True
    has_content = False
    option_spec = {
        "class": directives.class_option,
        "group": directives.unchanged,
        "title": directives.unchanged,
    }
    optional_arguments = 0
    required_arguments = 1

    ### PUBLIC METHODS ###

    def run(self):
        """Executes the directive.
        """
        node = thumbnail_block()
        node["classes"] += self.options.get("class", "")
        node["group"] = self.options.get("group", "")
        node["title"] = self.options.get("title", "")
        node["uri"] = self.arguments[0]
        environment = self.state.document.settings.env
        environment.images.add_file("", node["uri"])
        return [node]


class thumbnail_block(image, General, Element):
    __documentation_ignore_inherited__ = True


def visit_thumbnail_block_html(self, node):
    template = normalize(
        """
        <a data-lightbox="{group}" href="{target_path}" title="{title}" data-title="{title}" class="{cls}">
            <img src="{thumbnail_path}" alt="{alt}"/>
        </a>
        """
    )
    self.builder.thumbnails.add_file("", node["uri"])
    title = node["title"]
    classes = " ".join(node["classes"])
    group = "group-{}".format(node["group"] if node["group"] else node["uri"])
    if node["uri"] in self.builder.images:
        node["uri"] = os.path.join(
            self.builder.imgpath, self.builder.images[node["uri"]]
        )
    target_path = node["uri"]
    prefix, suffix = os.path.splitext(target_path)
    if suffix == ".svg":
        thumbnail_path = target_path
    else:
        thumbnail_path = "{}-thumbnail{}".format(prefix, suffix)
    output = template.format(
        alt=title,
        group=group,
        target_path=target_path,
        cls=classes,
        thumbnail_path=thumbnail_path,
        title=title,
    )
    self.body.append(output)
    raise SkipNode


def visit_thumbnail_block_latex(self, node):
    raise SkipNode


def on_builder_inited(app):
    app.builder.thumbnails = FilenameUniqDict()
    (pathlib.Path(app.builder.outdir) / "_images").mkdir(exist_ok=True)


class LilyPondExtension(Extension):
    class Kind(enum.Enum):
        IMAGE = 1
        AUDIO = 2

    class lilypond_block(General, FixedTextElement):
        pass

    @classmethod
    def setup_console(cls, console, monkeypatch):
        monkeypatch.setattr(
            Illustrator,
            "__call__",
            lambda self: console.push_proxy(
                cls(
                    self.illustrable,
                    cls.Kind.IMAGE,
                    **{
                        key.replace("lilypond/", "").replace("-", "_"): value
                        for key, value in console.proxy_options.items()
                        if key.startswith("lilypond/")
                    },
                ),
            ),
        )
        monkeypatch.setattr(
            Player,
            "__call__",
            lambda self: console.push_proxy(
                cls(
                    self.illustrable,
                    cls.Kind.AUDIO,
                    **{
                        key.replace("lilypond/", "").replace("-", "_"): value
                        for key, value in console.proxy_options.items()
                        if key.startswith("lilypond/")
                    },
                ),
            ),
        )

    @classmethod
    def setup_sphinx(cls, app):
        app.add_node(
            cls.lilypond_block,
            html=[cls.visit_block_html, None],
            latex=[cls.visit_block_latex, None],
            text=[cls.visit_block_text, cls.depart_block_text],
        )
        cls.add_option("lilypond/no-stylesheet", directives.flag)
        cls.add_option("lilypond/no-trim", directives.flag)
        cls.add_option("lilypond/pages", directives.unchanged)
        cls.add_option("lilypond/stylesheet", directives.unchanged)
        cls.add_option("lilypond/with-columns", int)

    def __init__(
        self,
        illustrable,
        kind,
        no_stylesheet=None,
        no_trim=None,
        pages=None,
        stylesheet=None,
        with_columns=None,
        **keywords,
    ):
        self.illustrable = copy.deepcopy(illustrable)
        self.keywords = keywords
        self.kind = kind
        self.no_stylesheet = no_stylesheet
        self.no_trim = no_trim
        self.pages = pages
        self.stylesheet = stylesheet
        self.with_columns = with_columns

    def to_docutils(self):
        illustration = self.illustrable.__illustrate__(**self.keywords)
        if self.kind == self.Kind.AUDIO:
            block = Block(name="midi")
            illustration.score_block.items.append(block)
        if illustration.header_block:
            if getattr(illustration.header_block, "tagline") is False:
                # default.ily stylesheet already sets tagline = ##f
                delattr(illustration.header_block, "tagline")
            if illustration.header_block.empty():
                illustration.items.remove(illustration.header_block)
        if illustration.layout_block and illustration.layout_block.empty():
            illustration.items.remove(illustration.layout_block)
        if illustration.paper_block and illustration.paper_block.empty():
            illustration.items.remove(illustration.paper_block)
        token = LilyPondVersionToken("2.19.83")
        illustration._lilypond_version_token = token
        stylesheet = self.stylesheet or "default.ily"
        if self.no_stylesheet:
            stylesheet = None
        if stylesheet and not illustration.includes:
            illustration._use_relative_includes = True
            includes = [stylesheet]
            illustration._includes = tuple(includes)
        code = format(illustration, "lilypond")
        node = self.lilypond_block(code, code)
        node["kind"] = self.kind.name.lower()
        node["no-stylesheet"] = self.no_stylesheet
        node["no-trim"] = self.no_trim
        node["pages"] = self.pages
        node["with-columns"] = self.with_columns
        return [node]

    @staticmethod
    def visit_block_html(self, node):
        output_directory = pathlib.Path(self.builder.outdir) / "_images"
        render_prefix = "lilypond-{}".format(
            hashlib.sha256(node[0].encode()).hexdigest()
        )
        if node["kind"] == "audio":
            flags = []
            glob = f"{render_prefix}.mid*"
        else:
            flags = ["-dcrop", "-dbackend=svg"]
            glob = f"{render_prefix}*.svg"
        lilypond_io = LilyPondIO(
            None,
            flags=flags,
            output_directory=output_directory,
            render_prefix=render_prefix,
            should_copy_stylesheets=True,
            should_open=False,
            should_persist_log=False,
            string=node[0],
        )
        if not list(output_directory.glob(glob)):
            _, _, _, success, log = lilypond_io()
            if not success:
                logger.warning(f"LilyPond render failed\n{log}", location=node)
        source_path = (pathlib.Path(self.builder.imgpath) / render_prefix).with_suffix(
            ".ly"
        )
        if node["kind"] == "audio":
            pass
        else:
            embed_images(self, node, output_directory, render_prefix, source_path)
        raise SkipNode


table_row_open_template = '<div class="table-row">'
table_row_close_template = "</div>"
basic_image_template = normalize(
    """
    <div class="uqbar-book">
        <a href="{source_path}"><img src="{relative_path}"/></a>
    </div>
    """
)
thumbnail_template = normalize(
    """
    <a data-lightbox="{group}" href="{fullsize_path}" title="{title}" data-title="{title}" class="{cls}">
        <img src="{thumbnail_path}" alt="{alt}"/>
    </a>
    """
)


def embed_images(self, node, output_directory, render_prefix, source_path):
    paths_to_embed = []
    if node.get("pages"):
        for page_spec in node["pages"].split(","):
            page_spec = page_spec.strip()
            if "-" in page_spec:
                start_spec, _, stop_spec = page_spec.partition("-")
                start_page, stop_page = int(start_spec), int(stop_spec) + 1
            else:
                start_page, stop_page = int(page_spec), int(page_spec) + 1
            for page_number in range(start_page, stop_page):
                for path in output_directory.glob(f"{render_prefix}-{page_number}.svg"):
                    paths_to_embed.append(path)
    elif node.get("no-trim"):
        for path in output_directory.glob(f"{render_prefix}.svg"):
            paths_to_embed.append(path)
        if not paths_to_embed:
            page_count = len(list(output_directory.glob(f"{render_prefix}-*.svg")))
            for page_number in range(1, page_count + 1):
                for path in output_directory.glob(f"{render_prefix}-{page_number}.svg"):
                    paths_to_embed.append(path)
    else:
        for path in output_directory.glob(f"{render_prefix}.cropped.svg"):
            paths_to_embed.append(path)
    with_columns = node.get("with-columns")
    if with_columns:
        for i in range(0, len(paths_to_embed), with_columns):
            self.body.append(table_row_open_template)
            for path in paths_to_embed[i:i + with_columns]:
                relative_path = pathlib.Path(self.builder.imgpath) / path.name
                self.body.append(thumbnail_template.format(
                    alt="",
                    cls="table-cell thumbnail",
                    group=f"group-{render_prefix}",
                    fullsize_path=relative_path,
                    thumbnail_path=relative_path,
                    title="",
                ))
            self.body.append(table_row_close_template)
    else:
        for path in paths_to_embed:
            relative_path = pathlib.Path(self.builder.imgpath) / path.name
            self.body.append(
                basic_image_template.format(
                    relative_path=relative_path, source_path=source_path
                )
            )


def setup(app):
    app.connect("builder-inited", on_builder_inited)
    app.add_directive("docs", HiddenDoctestDirective)
    app.add_directive("shell", ShellDirective)
    app.add_directive("thumbnail", ThumbnailDirective)
    app.add_node(
        thumbnail_block,
        html=[visit_thumbnail_block_html, None],
        latex=[visit_thumbnail_block_latex, None],
    )
