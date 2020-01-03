# znavot
A Python script for searching MediaWiki dumps for link trails

This is a very initial version, which barely works for the Hebrew Wikipedia.

This version is super-bare. I’m just trying to release early and often.
I’ll add running instructions, better error handling, support for other languages
and other much-needed features some time later.

# Installation
Before running, install pywikibot:
    pip3 install pywikibot

This repo includes a dummy user-config.py, which should be enough
for processing the dump.

# Invoking
    python3 znavot.py [-h] [--stop_after STOP_AFTER] dump_filename

`--stop_after` is useful if you want to quickly test without processing
the whole big dump file.

Use the XXwiki-YYYYMMDD-pages-articles.xml dump from
[Wikimedia Downloads](http://download.wikimedia.org/).

Author: Amir E. Aharoni

License: GPL 3.0

Thanks to the tireless Ladsgroup for the help with starting this project up.
