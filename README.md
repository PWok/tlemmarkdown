# Markdown formatter for use by The League of Extraordinary Minds
(and an excuse for me to learn [poetry](https://python-poetry.org) )

-------

## Instalation
For use with [python poetry](https://python-poetry.org) download the repository and initalize poetry.

You can also install with pip using either
```bash
pip install git+https://github.com/PWok/tlemmarkdown.git
```
to install the newest version or
```bash
pip install https://github.com/PWok/tlemmarkdown/releases/download/v0.1.1/tlemmarkdown-0.1.1.tar.gz
```
to install from a release and a specified archive type.

## Usage
Run `python3 ./tlemmarkdown -h` for a help menu

Current command line arguments include:
- `-s` to set source markdown file
- `-o` to set output file
- `-c` to set code highlighting style. Any Pygments-supported style can be used. (defaults to monokai)

\+ `--source-encoding` and `--output-encoding`. Defaults to UTF-8

Example usage:
```bash
python3  ./tlemmarkdown -s build/testmd.md -o build/test.html
```

## Syntax
The markdown syntax used is the default syntax of [python markdown](https://python-markdown.github.io/) (so basically the original markdown syntax), with the following modifications:
- lists are *saner* (see [sane lists](https://python-markdown.github.io/extensions/sane_lists/))
- new lines are changed to `</br>` tags (see [nl2br](https://python-markdown.github.io/extensions/nl2br/))
- `--` and `---` in text are changed into `&ndash;` and `&mdash;` respectively
- `__text__` underlines the text insted of bolding it (<u>text</u> instead of **text**)
- `~~text~~` acts as strikethrough (so <del>text</del> is the result)
- images have style set to `width: 100%;`
- text between `[task]` and `[/task]` tags is put inside the tlem pink task box and between `[info]` and `[/info]` &ndash; inside the grey info block.
    - the tags have to appear at the start of a line. No other text (other than whitespace) can be on the same line
    - the tags are case insensitive (meaning either of `[task]`, `[TASK]` or `[taSK]` will work) but the starting and ending tag have to be styled consitently (you cannot start a block with a `[info]` and close it with `[/INFO]`. It just won't work)
- text with the code fence (<code>```</code>) is treated as code. No other markdown is applied to it. Opening and closing fences have to appear at the beggining of a line. No other (non-whitespace) text may appear at the same line as the closing fence. Any text at the same line as the opening fence will be treated as the name of the language in which the following code is written. It will be used for syntax highlighting. The folowing is an example codefence:
````
```python
from random import Random
inst = Random
print(inst.randrange(1000))
```
````