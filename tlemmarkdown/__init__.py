import markdown

from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import HtmlFormatter

code = 'print "Hello World"'
print(highlight(code, Python3Lexer(), HtmlFormatter()))