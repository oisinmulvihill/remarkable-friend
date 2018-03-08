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

pipenv install

## running tests

pipenv run pytest -s --pdb
