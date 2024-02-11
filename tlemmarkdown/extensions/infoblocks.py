import re
import xml.etree.ElementTree as etree

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension

# Options
# ~~~~~~~

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = True


class TlemCodeTaskBlockProcessor(BlockProcessor):

    PATTERN_START = re.compile(r"""^\[[tT][aA][sS][kK]\][ ]*\n""", re.M)
    PATTERN_END = re.compile(r"""\[/[tT][aA][sS][kK]\][ ]*$""", re.M)

    style_data = "background:#edd;border:1px solid #caa;padding:5px 10px;"

    def test(self, parent, block):
        return self.PATTERN_START.search(block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        m = self.PATTERN_START.search(blocks[0])
        pre_block = [f"{blocks[0][:m.start()]}"]
        blocks[0] = f"{blocks[0][m.end():]}"
        # Find block with ending tag
        for block_num, block in enumerate(blocks):
            if self.PATTERN_END.search(block):
                # remove
                blocks[block_num] = self.PATTERN_END.sub("", block)
                # render tagged area inside a new div
                pre_e = etree.SubElement(parent, "p")
                self.parser.parseBlocks(pre_e, pre_block)
                e = etree.SubElement(parent, "div")
                e.set("style", self.style_data)
                self.parser.parseBlocks(e, blocks[0 : block_num + 1])
                # remove used blocks
                for _ in range(0, block_num + 1):
                    blocks.pop(0)
                return True
        blocks[0] = original_block
        return False


class TlemCodeTaskExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            TlemCodeTaskBlockProcessor(md.parser), "TlemCodeTaskBlockProcessor", 26
        )
