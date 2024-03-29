"""
    Markdown Preprocessor code fence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Adapted from 
    https://github.com/pygments/pygments/blob/master/external/markdown-processor.py
    and
    https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/fenced_code.py
    
"""

import re

from textwrap import dedent

import markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter  # pylint: disable=E0611
from pygments.lexers import get_lexer_by_name, TextLexer  # pylint: disable=E0611
from pygments.style import Style


# Options
# ~~~~~~~

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = True


class TlemCodeFencePreprocessor(Preprocessor):

    PATTERN = re.compile(
        dedent(
            r"""
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*                          # opening fence
            (\.?(?P<lang>[\w\d#.+-]*)[ ]*)?                          # optional (.)lang
            \n                                                       # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                                     # the code block
            (?P=fence)[ ]*$                                          # closing fence
        """
        ),
        re.MULTILINE | re.DOTALL | re.VERBOSE,
    )

    style_data = '''style="background:#141414;border:1px solid #ccc;color:#E9F8F8;font-family:monospace;font-size:11px;padding:5px 10px;"'''

    def __init__(self, md: markdown.Markdown, code_style: str | type[Style] = "monokai"):
        if code_style is None:
            code_style = "monokai"
        self.formatter = HtmlFormatter(
            nowrap=True,
            noclasses=INLINESTYLES,
            style=code_style,
            wrapcode=False,
        )
        super().__init__(md)

    def run(self, lines):

        text = "\n".join(lines)
        while True:
            m = self.PATTERN.search(text)
            if m:
                try:
                    lexer = get_lexer_by_name(m.group("lang"))
                except pygments.util.ClassNotFound:
                    lexer = TextLexer()
                code = highlight(m.group("code"), lexer, self.formatter)
                code = code.replace("\n\n", "\n&nbsp;\n").replace("\n", "<br />")
                code = f'<div {self.style_data} class="code">{code}</div>'
                placeholder = self.md.htmlStash.store(code)
                text = f"{text[:m.start()]}\n{placeholder}\n{text[m.end():]}"
            else:
                break

        return text.split("\n")


class TlemCodeFenceExtension(Extension):
    def __init__(self, code_style: str | type[Style] = "monokai", **kwargs) -> None:
        self.code_style = code_style
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.preprocessors.register(
            TlemCodeFencePreprocessor(md, self.code_style),
            "TlemCodeFencePreprocessor",
            25,
        )
