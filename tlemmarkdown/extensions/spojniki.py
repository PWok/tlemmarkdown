import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

nbsp = "&nbsp;"
spojniki = ["a", "i", "o", "z", "w", "u", "że", "A", "I", "O", "Z", "W", "U"]

patterns = [rf"([\s{nbsp}([{{\-–])({i}\s)" for i in spojniki]
replacements = [rf"\1{i}{nbsp}" for i in spojniki]

pairs = list(zip(patterns, replacements))


class SpojnikiPreprocessor(Preprocessor):

    def run(self, lines):

        text = "\n".join(lines)
        for p, r in pairs:
            text = re.sub(p, r, text)

        return text.split("\n")


class SpojnikiExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(
            SpojnikiPreprocessor(md),
            "SpojnikiPreprocessor",
            24,
        )
