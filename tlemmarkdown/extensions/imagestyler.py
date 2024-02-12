from markdown import Extension, Markdown
from markdown.treeprocessors import Treeprocessor


class TlemImageStyler(Treeprocessor):

    max_width_style = "width: 100%;"

    def run(self, root):
        images = root.findall("img")
        for img in images:
            style = img.get("style")
            if style is None:
                style = ""
            img.set("style", style + self.max_width_style)
        
        for elem in root:
            self.run(elem)


class TlemImageStylerExtension(Extension):
    def extendMarkdown(self, md: Markdown):
        md.treeprocessors.register(TlemImageStyler(), "TlemImageStyler", 15)
