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

 - https://plasma.ninja/blog/devices/remarkable/binary/format/2017/12/26/reMarkable-lines-file-format.html

# Development

## Environment


Create the rmfriend virtualenv. In my case I do this with virtualenvwrapper:

```bash

mkvirtualenv -p python3 rmfriend

```

Then install the requirements and set up the rmfriend console script as follows:

```bash

# activate the virtualenv. In my case:
workon rmfriend

make install

```


## running tests

Once the environment is activated and set up you can run all the tests as follows:

```bash

make test

```


## Usage


### Convert a Notebook to SVG

I've produced a very basic converter takes the path to a transferred notebook
and the base output file name. Each page will be converted to its own SVG
drawing. My goal here is to produce a preview I can later use when moving

```bash

$rmfriend notebook_to_svg tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines  out
2018-03-10 15:53:51,917 do_notebook_to_svg DEBUG Reading file 'tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines'
2018-03-10 15:53:51,918 do_notebook_to_svg DEBUG Parsing file 'tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines'

2018-03-10 15:53:51,931 do_notebook_to_svg DEBUG tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines has '1' pages.
2018-03-10 15:53:51,943 do_notebook_to_svg DEBUG Writing file 'out-00.svg'.

oisin@tarsis [remarkable-friend]
$

```

The out-00.svg should look like:
![out-00.svg](https://github.com/oisinmulvihill/remarkable-friend/raw/master/out-00.svg "out-00.svg")


### Convert a Notebook to PNG

This is a very rudimentary converter from lines format to PNG. It works but
needs a lot more work.

```bash

$rmfriend notebook_to_png tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines  out
2018-03-10 15:53:26,660 do_notebook_to_png DEBUG Reading file 'tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines'
2018-03-10 15:53:26,661 do_notebook_to_png DEBUG Parsing file 'tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines'

2018-03-10 15:53:26,674 do_notebook_to_png DEBUG tests/examples/b8c0aaa8-decb-4d39-9218-b66a7418aef9.lines has '1' pages.
2018-03-10 15:53:26,688 do_notebook_to_png DEBUG Writing file 'out-00.png'.

oisin@tarsis [remarkable-friend]
$ls *.png
out-00.png


```

The out-00.png should look like:
![out-00.png](https://github.com/oisinmulvihill/remarkable-friend/raw/master/out-00.png "out-00.png")
