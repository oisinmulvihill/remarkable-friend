# reMarkable Friend

This aims to allow the manipulation reMarkable notebooks on a desktop machine.

My first goal is to be able to copy pages from one notebook to another.
Currently I'm working on the parsing of the file into an intermediate
structure to aid manipulation. Once complete I should be able to write the
format back to disk. This opens the possiblity to generate lines files.

I aim later to be able to write SVG/PNG files from the parsed input. However
I'd also like to be able to convert SVG files into lines formatted files. This
should be possible soon.

I've been inspired by the hard work of the following projects which worked-out
the reMarkable lines file format.

 - https://github.com/reHackable/maxio

 - https://github.com/ax3l/lines-are-beautiful

 - https://plasma.ninja/blog/devices/remarkable/binary/format/2017/12/26/
    reMarkable-lines-file-format.html

# Development

## Environment

make install


## Usage


### Convert a Notebook to SVG

I've produced a very basic converter takes the path to a transferred notebook
and the base output file name. Each page will be converted to its own SVG
drawing. My goal here is to produce a preview I can later use when moving

```

$ pipenv run rmfriend notebook_to_svg tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines  out
2018-03-10 15:23:05,184 do_notebook_to_svg rmfriend.tools.admincommands.do_notebook_to_svg DEBUG Reading file 'tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines'
2018-03-10 15:23:05,184 do_notebook_to_svg rmfriend.tools.admincommands.do_notebook_to_svg DEBUG Parsing file 'tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines'

2018-03-10 15:23:05,198 do_notebook_to_svg rmfriend.tools.admincommands.do_notebook_to_svg DEBUG tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines has '1' pages.

$

```

### Convert a Notebook to PNG

Comming soon.


## running tests

pipenv run pytest -s --pdb
