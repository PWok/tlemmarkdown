import sys
import markdown
from markdown.extensions.smarty import SmartyExtension

from . import extensions


def main(source, output, *, source_encoding, output_encoding, code_style="monokai"):
    try:
        if source is None:
            html = input()
        else:
            exts = [
                extensions.TlemFence(code_style),
                extensions.TlemUnderline(),
                extensions.TlemDel(),
                extensions.TlemTask(),
                extensions.TlemInfo(),
                SmartyExtension(smart_ellipses=False, smart_quotes=False),
                "sane_lists",
                "nl2br",
                # "tables", # We don't REALLY use tables...
            ]
            with open(source, "r", encoding=source_encoding) as f:
                # html = markdown.markdown(f.read())
                html = markdown.markdown(f.read(), extensions=exts)

        if output is None:
            print(html)
        else:
            with open(output, "w", encoding=output_encoding) as f:
                f.write(html)
        return 0
    except Exception as e:
        sys.exit(e)
