import re
import xml.etree.ElementTree as etree

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension

# Options
# ~~~~~~~

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = True


class TlemTaskBlockProcessor(BlockProcessor):

    PATTERN_START = re.compile(r"""^\[(?P<name>task)\][ ]*\n""", re.M | re.I)
    RAW_PATTERN_END = r"""\[/{}\][ ]*$"""
    # PATTERN_END = re.compile(, re.M)

    style_data = "background:#edd;border:1px solid #caa;padding:5px 10px;"

    def test(self, parent, block):
        return self.PATTERN_START.search(block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        m = self.PATTERN_START.search(blocks[0])
        PATTERN_END = re.compile(self.RAW_PATTERN_END.format(m.group("name")), re.M)

        pre_block = blocks[0][: m.start()].strip("\n")
        blocks[0] = f"{blocks[0][m.end():]}"
        # Find block with ending tag
        for block_num, block in enumerate(blocks):
            if PATTERN_END.search(block):
                # remove
                post_m = PATTERN_END.search(block)
                blocks[block_num] = block[: post_m.start()]
                post_block = block[post_m.end() :]

                # add text in block before tag as <p>
                if pre_block:
                    # we add the text directly to parent div
                    # adding it in a <p> subelement caused weird formatting and empty <p> tags...
                    self.parser.parseBlocks(parent, [pre_block])
                # add tagged area
                e = etree.SubElement(parent, "div")
                e.set("style", self.style_data)
                self.parser.parseBlocks(e, blocks[0 : block_num + 1])
                # remove used blocks and add post_block as first block
                for _ in range(0, block_num):
                    blocks.pop(0)
                blocks[0] = post_block
                return True
        blocks[0] = original_block
        return False


class TlemTaskExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            TlemTaskBlockProcessor(md.parser), "TlemCodeTaskBlockProcessor", 26
        )


# The folowing code is literally the same as above, but every mention of `task` was replaced with `info`
# And the background colour of the div element was changed 
class TlemInfoBlockProcessor(BlockProcessor):

    PATTERN_START = re.compile(r"""^\[(?P<name>info)\][ ]*\n""", re.M | re.I)
    RAW_PATTERN_END = r"""\[/{}\][ ]*$"""
    # PATTERN_END = re.compile(, re.M)

    style_data = "background:#eee;border:1px solid #ccc;padding:5px 10px;"

    def test(self, parent, block):
        return self.PATTERN_START.search(block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        m = self.PATTERN_START.search(blocks[0])
        PATTERN_END = re.compile(self.RAW_PATTERN_END.format(m.group("name")), re.M)

        pre_block = blocks[0][: m.start()].strip("\n")
        blocks[0] = f"{blocks[0][m.end():]}"
        # Find block with ending tag
        for block_num, block in enumerate(blocks):
            if PATTERN_END.search(block):
                # remove
                post_m = PATTERN_END.search(block)
                blocks[block_num] = block[: post_m.start()]
                post_block = block[post_m.end() :]

                # add text in block before tag as <p>
                if pre_block:
                    # we add the text directly to parent div
                    # adding it in a <p> subelement caused weird formatting and empty <p> tags...
                    self.parser.parseBlocks(parent, [pre_block])
                # add tagged area
                e = etree.SubElement(parent, "div")
                e.set("style", self.style_data)
                self.parser.parseBlocks(e, blocks[0 : block_num + 1])
                # remove used blocks and add post_block as first block
                for _ in range(0, block_num):
                    blocks.pop(0)
                blocks[0] = post_block
                return True
        blocks[0] = original_block
        return False


class TlemInfoExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            TlemInfoBlockProcessor(md.parser), "TlemCodeInfoBlockProcessor", 27
        )
