import sys
import argparse

from tlemmarkdown import main


def run():
    parser = argparse.ArgumentParser(
        description="Read a markdown file and process it to an html file as used by T-LEM"
    )
    parser.add_argument(
        "-s",
        "--source",
        dest="source",
        type=str,
        default=None,
        help="The markdown file. Stdin by default",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        default=None,
        help="The resulting html file. Stdout by default.",
    )
    parser.add_argument(
        "-c",
        "--code-style",
        dest="code_style",
        type=str,
        default="monokai",
        help="""Optional code style name. Can be any style supported by Pygments
                Defaults to monokai. It should be noted that the background is overwritten.
                By default the `C++ code` black (hex #141414) background, causing some styles to be unreadble""",
    )
    parser.add_argument(
        "--source-encoding",
        dest="source_encoding",
        type=str,
        default="UTF-8",
        help="The text encoding of the source file.",
    )
    parser.add_argument(
        "--output-encoding",
        dest="output_encoding",
        type=str,
        default="UTF-8",
        help="The text encoding of the output file.",
    )
    parser.add_argument(
        "--no-spoj",
        dest="no_spoj",
        action="store_true",
        default=False,
        help="Wheter to add non-breaking space (&nbsp;) after one lettter words. Switch on/off. Defaults to on.",
    )

    args = parser.parse_args()
    sys.exit(
        main(
            args.source,
            args.output,
            source_encoding=args.source_encoding,
            output_encoding=args.output_encoding,
            code_style=args.code_style,
            no_spoj=args.no_spoj,
        )
    )


if __name__ == "__main__":
    run()
