"""
    Markdown Preprocessor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Adapted from: 
    https://github.com/pygments/pygments/blob/master/external/markdown-processor.py
    
"""

import re

from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

from pygments import highlight
from pygments.formatters import HtmlFormatter  # pylint: disable=E0611
from pygments.lexers import get_lexer_by_name, Python3Lexer  # pylint: disable=E0611
from pygments.styles import get_style_by_name


# Options
# ~~~~~~~

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = True


class CodeBlockPreprocessor(Preprocessor):

    pattern = re.compile(r"\`\`\`(\w*)\n([^\`]*)\`\`\`")

    formatter = HtmlFormatter(
        nowrap=True,
        noclasses=INLINESTYLES,
        style=get_style_by_name("monokai"),
        wrapcode=False,
    )

    code_tag_data = '''style="background:#141414;border:1px solid #ccc;color:#E9F8F8;font-family:monospace;font-size:11px;padding:5px 10px;"'''

    def run(self, lines):
        def repl(m):
            try:
                lexer = get_lexer_by_name(m.group(1))
            except ValueError:
                lexer = Python3Lexer()
            code = highlight(m.group(2), lexer, self.formatter)
            code = code.replace("\n\n", "\n&nbsp;\n").replace("\n", "<br />")
            res = f'\n\n<div {self.code_tag_data} class="code">{code}</div>\n\n'
            return res

        joined_lines = "\n".join(lines)
        joined_lines = self.pattern.sub(repl, joined_lines)
        return joined_lines.split("\n")


class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(CodeBlockPreprocessor(), "CodeBlockPreprocessor", 999)
