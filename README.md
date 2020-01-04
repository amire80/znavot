# znavot
A Python script for searching MediaWiki dumps for link trails

This is a very initial version, which barely works for the Hebrew Wikipedia.

This version is super-bare. I’m just trying to release early and often.
I’ll add running instructions, better error handling, support for other languages
and other much-needed features some time later.

# Installation
Before running, install the required packages:
    pip3 install -r requirements.txt

This repo includes a dummy `user-config.py`, which should be enough
for processing the dump. In the future it will probably have real configuration
to allow uploading of page lists.

# Invoking
    python3 znavot.py [-h] [--stop_after STOP_AFTER] dump_filename

`--stop_after` is useful if you want to quickly test without processing
the whole big dump file.

# Input
## Content
Use the `XXwiki-YYYYMMDD-pages-articles.xml` dump from
[Wikimedia Downloads](http://download.wikimedia.org/).

It's recommended to put dump files in `dumps/` while processing,
so that there would be fewer non-code files in the main directory.

## Common trails
Every language has a list of trails that are common and valid, and that
don't need to be processed and counted. They are listed in a file in
the `common_trails` directory. The file is a simple text file with one trail
per line, and the file name is LANGUAGE_CODE.txt.

The script takes the language code from the `--language` argument.
If it's not given, it tries to figure it out from the dump file name,
and if this fails, too, the script exits with an error.

# Output
The output goes to the TRAILS_OUT directory.

The file `_single_trails.txt` includes trails that were only found once.

The file `_problematic_trails.txt` includes trails that couldn't be used for
file names.

Each of the other trails gets a file called `trail_X_TRAIL_titles.txt`,
where X is an index and TRAIL is the trail itself.

## Special characters handling
Some trail characters that are hard to put in filenames are automatically
replaced with ASCII names. For a full list see the file
`special_characters.yaml`.

In the text of the output file itself, these characters are written explicitly
in double quotes.

If you find more problematic characters that aren't here and you want
to understand what they are,
[Richard Ishida's UniView tool](https://r12a.github.io/uniview/)
is recommended. Paste the text, click the arrow down button, and you'll
see the Unicode character names at the bottom. Patches welcome!

# Credits
Author: Amir E. Aharoni

License: GPL 3.0

Thanks to the tireless Ladsgroup for the help with starting this project up.
