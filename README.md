# reMarkable Friend [![Build Status](https://travis-ci.org/oisinmulvihill/remarkable-friend.svg?branch=master)](https://travis-ci.org/oisinmulvihill/remarkable-friend)

This allows the manipulation reMarkable notebooks on a desktop machine. It also
allows notebooks to be backed-up to your desktop computer.

# Table of contents
1. [Development](#development)
2. [Usage](#usage)
    1. [reMarkable Sync](#rsync)
        1. [Dropbox / Cloud Backup](#cloudbackup)
    2. [Notebook listing](#ls)
    3. [Notebook to SVG](#to_svg)
    4. [Notebook to SVG](#to_png)

# Development <a name="development"></a>

## Updates

Notebooks can now by backed-up to the desktop see [reMarkable Sync](#rsync) for
more details.

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

## UI

For the GUI and MacOSX app see the frontend repository:

 - https://github.com/oisinmulvihill/remarkable-friend-ui


# Usage <a name="usage"></a>

The following are the reMarkable Friend action which can be used from the
command line.

The first time command line `rmfriend` is run it creates a `.rmfriend`
directory in your home. Inside the configuration file `config.cfg` is created
along with the `notebooks` cache directory.

## reMarkable Sync <a name="rsync"></a>

This command will synchronise the notebooks with your desktop computer. For
example:

```bash

$ rmfriend rsync
All notebooks on reMarkable: 43
Notebooks only present locally: 1
Notebooks on both: 44
Notebooks only on reMarkable: 0
Working out changes: 100%

$

```

The first time this will recover all the notebooks and make take some time. Later
runs will be faster as only what has changed will be synchronised.

If a notebook is deleted from reMarkable it will not be deleted locally. I
favour this approach. I can restore a notebook if I want to.

### Backup to Dropbox / Google Drive <a name="cloudbackup"></a>

You could backup your notebooks to Dropbox, Google Drive or any other cloud
provider by changing the cache_dir configuration option. To do this edit the
file `~/.rmfriend/config.cfg` and change `cache_dir`.

For example for Dropbox I would do:

```bash

$ vi ~/.rmfriend/config.cfg

[rmfriend]
:
cache_dir = /Users/oisin/Dropbox/notebooks
:

```

Only one cache_dir is supported.

## List notebooks <a name="ls"></a>

This is used to see what notebooks are present on reMarkable. It also shows
the latest version for each notebook. If the notebook is cached locally then
the local version will be displayed as well.

Using -p/--password will ask for the password to be entered in a secure way. You
can use -a/--address to change where to connect. To see the raw document UUID
you can add --show-id.

```bash

$rmfriend ls --password
Please enter password for root@10.99.11.1:
+---------------------+--------------------------------+--------------------+---------------+
| Last Modified       | Name                           | reMarkable Version | Local Version |
+---------------------+--------------------------------+--------------------+---------------+
| 2018-04-06 12:59:24 | Unmortgage                     | 28                 | 28            |
| 2018-02-13 21:17:50 | Tech Dinner                    | 2                  | 2             |
:
etc
:
| 2018-03-11 12:16:54 | Asia 2018                      | 30                 | 30            |
| 2018-03-02 14:29:40 | Research                       | 12                 | 12            |
+---------------------+--------------------------------+--------------------+---------------+

$

```

Outdated video:

![listing notebooks](https://github.com/oisinmulvihill/rmfriend-releases/raw/master/image/listing-notebooks.gif "listing-notebooks.gif")


## Convert a Notebook to SVG <a name="to_svg"></a>

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


## Convert a Notebook to PNG <a name="to_png"></a>

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
