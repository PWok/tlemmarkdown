import sys
import argparse

from tlemmarkdown import main

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
    "--source-encoding",
    dest="source_encoding",
    type=str,
    default="UTF-8",
    help="The text encoding of the source file.",
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
    "--output-encoding",
    dest="output_encoding",
    type=str,
    default="UTF-8",
    help="The text encoding of the output file.",
)

args = parser.parse_args()
sys.exit(
    main(
        args.source,
        args.output,
        source_encoding=args.source_encoding,
        output_encoding=args.output_encoding,
    )
)
