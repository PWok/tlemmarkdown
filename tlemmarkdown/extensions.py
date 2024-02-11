"""
    Markdown Preprocessor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Adapted from: 
    https://github.com/pygments/pygments/blob/master/external/markdown-processor.py
    
"""

import re

from textwrap import dedent

import markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter  # pylint: disable=E0611
from pygments.lexers import get_lexer_by_name, Python3Lexer  # pylint: disable=E0611
from pygments.styles import get_style_by_name


# Options
# ~~~~~~~

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = True


class CodeBlockPreprocessor(Preprocessor):

    PATTERN = re.compile(
        dedent(r'''
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*                          # opening fence
            (\.?(?P<lang>[\w\d#.+-]*)[ ]*)?                          # optional (.)lang
            \n                                                       # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                                     # the code block
            (?P=fence)[ ]*$                                          # closing fence
        '''),
        re.MULTILINE | re.DOTALL | re.VERBOSE
    )

    formatter = HtmlFormatter(
        nowrap=True,
        noclasses=INLINESTYLES,
        style=get_style_by_name("monokai"),
        wrapcode=False,
    )

    code_tag_data = '''style="background:#141414;border:1px solid #ccc;color:#E9F8F8;font-family:monospace;font-size:11px;padding:5px 10px;"'''

    def __init__(self, md: markdown.Markdown):
        super().__init__(md)

    def run(self, lines):

        text = "\n".join(lines)
        while True:
            m = self.PATTERN.search(text)
            if m:
                try:
                    lexer = get_lexer_by_name(m.group("lang"))
                except pygments.util.ClassNotFound:
                    lexer = Python3Lexer()
                code = highlight(m.group("code"), lexer, self.formatter)
                code = code.replace("\n\n", "\n&nbsp;\n").replace("\n", "<br />")
                code = f'\n\n<div {self.code_tag_data} class="code">{code}</div>\n\n'
                placeholder = self.md.htmlStash.store(code)
                text = f'{text[:m.start()]}\n{placeholder}\n{text[m.end():]}'
            else:
                break

        return text.split("\n")


class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(CodeBlockPreprocessor(md), "CodeBlockPreprocessor", 25)
