import sys
import markdown

from .extensions import CodeBlockExtension


def main(source, output, *, source_encoding, output_encoding):
    try:
        if source is None:
            html = input()
        else:
            with open(source, "r", encoding=source_encoding) as f:
                # html = markdown.markdown(f.read())
                html = markdown.markdown(f.read(), extensions=[CodeBlockExtension()])

        if output is None:
            print(html)
        else:
            with open(output, "w", encoding=output_encoding) as f:
                f.write(html)
        return 0
    except Exception as e:
        sys.exit(e)
