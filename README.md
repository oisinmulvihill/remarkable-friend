# reMarkable Friend [![Build Status](https://travis-ci.org/oisinmulvihill/remarkable-friend.svg?branch=master)](https://travis-ci.org/oisinmulvihill/remarkable-friend)

This allows the manipulation reMarkable notebooks on a desktop machine.

![listing notebooks](https://github.com/oisinmulvihill/rmfriend-releases/raw/master/image/listing-notebooks.gif "listing-notebooks.gif")

For the GUI and MacOSX app see the frontend repository:

 - https://github.com/oisinmulvihill/remarkable-friend-ui

I have successfully implemented copying pages from an existing notebook into a
new one. Don't get too excited just yet, as I've only demonstrated this in my
unit tests. I need to wire this into the "rmfriend" command line tool as a
demonstration. I've also discovered that the reMarkable interface needs to
be restarted in order pickup new notebooks transferred to it. You could restart
reMarkable however that is slower. Currently I just manually do::

	# I've key exchanged so I don't need a password:
	ssh root@10.11.99.1 systemctl restart xochitl

I can now read and write a notebooks. Notebooks consist of a series of files
which have the same UUID filename but with different extensions. I read/write
metadata, content and lines (raw drawing information) files. I currently also
read the thumbnails and cache directories. I've also implemented rudimentaty rendering of notebook lines files to SVG or PNG images.

I'm also working on the syncronisation of notebooks from reMarkable to a cache
stored on the desktop. I was originally generate the PNG previews for the
remarkable-friend-ui, however this has proved to slow. I'm going to sync the
cache/thumbnails the reMarkable generates. I can then use these in the frontend
instead.

I've been inspired by the hard work of the following projects which worked-out
the reMarkable lines file format.

 - https://github.com/reHackable/maxio

 - https://github.com/ax3l/lines-are-beautiful

 - https://plasma.ninja/blog/devices/remarkable/binary/format/2017/12/26/reMarkable-lines-file-format.html

# Development

I'm currently developing on MacOSX using Python 3 installed from home brew. I
aim to produce stand alone program you can download for Mac, Linux and Windows
but thats a while a way yet.

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


### List notebooks from the command line

Using -p/--password will ask for the password to be entered in a secure way. You
can use -a/--address to change where to connect. To see the raw document UUID
you can add --show-id.

```bash

$rmfriend ls --password
Please enter password for root@10.99.11.1:
2018-03-13 21:34:11,796 connect INFO Connecting to device hostname '10.99.11.1' username 'root'
2018-03-13 21:34:12,443 connect INFO Connected to device '10.99.11.1' changing to remote path '/home/root/.local/share/remarkable/xochitl'
+---------------------+-------------------------------------+
| Last Modified       | Name                                |
+---------------------+-------------------------------------+
| 2018-02-13 21:17:50 | Tech Dinner                         |
| 2018-03-07 11:02:43 | Dev Process                         |
:
etc
:
| 2018-02-20 17:15:45 | Notes From "The Managers Path"      |
| 2018-03-08 09:22:56 | ForStandUp                          |
|---------------------+-------------------------------------+
2018-03-13 21:34:13,094 connect INFO Connection to device '10.99.11.1' closed.

$

```


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
