import sys
import markdown
from markdown.extensions.smarty import SmartyExtension

from . import extensions


def main(
        source, output, *, source_encoding,
        output_encoding, code_style="monokai", no_spoj=False
    ):
    try:
        if source is None:
            html = input()
        else:
            with open(source, "r", encoding=source_encoding) as f:
                html = f.read()

        exts = [
            extensions.TlemFence(code_style),
            extensions.TlemUnderline(),
            extensions.TlemDel(),
            extensions.TlemTask(),
            extensions.TlemInfo(),
            extensions.TlemImage(),
            SmartyExtension(smart_ellipses=False, smart_quotes=False),
            "sane_lists",
            "nl2br",
            # "tables", # We don't REALLY use tables...
        ]

        if not no_spoj:  # Who doesn't love double negation?
            print("rfegd")
            exts.append(extensions.TlemSpoj())

        html = markdown.markdown(html, extensions=exts)

        if output is None:
            print(html)
        else:
            with open(output, "w", encoding=output_encoding) as f:
                f.write(html)
        return 0
    except Exception as e:
        sys.exit(e)
