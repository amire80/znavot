#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import re
from pywikibot import xmlreader
from yaml import load
try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import Loader as YamlLoader

with open('special_characters.yaml', 'r') as special_characters_file:
    special_char_replacements = load(
        special_characters_file,
        Loader=YamlLoader
    )
for special_char in special_char_replacements:
    special_char_replacements[special_char] = (
        'EXPLICIT_' + special_char_replacements[special_char]
    )


def replace_special_chars(trail):
    escaped_trail = trail

    for special_char in special_char_replacements:
        escaped_trail = escaped_trail.replace(
            special_char,
            special_char_replacements[special_char]
        )

    return escaped_trail


argparser = argparse.ArgumentParser()

argparser.add_argument(
    "dump_filename",
    help="the name of the dumpfile you want to process"
)

argparser.add_argument(
    "--stop_after",
    action="store",
    type=int,
    help="after how many pages to stop the processing"
)

argparser.add_argument(
    "--language",
    action="store",
    help="language code"
)

args = argparser.parse_args()

if args.language:
    language = args.language
else:
    language_code_captures = re.findall(r'([a-z-]+)wiki', args.dump_filename)
    if len(language_code_captures) != 1:
        print('Cannot figure out the language code from the dump filename. ' +
              'Please provide one explicitly using --language.')
        exit(1)
    language = language_code_captures[0]

dump = xmlreader.XmlDump(args.dump_filename)

common_trails_dir = 'common_trails'
common_trails = {}
common_trails_filename = common_trails_dir + '/' + language + '.txt'
common_trails_file = open(
    common_trails_filename,
    encoding='utf-8',
    mode='r'
)

for line in common_trails_file:
    common_trails[line.rstrip(os.linesep)] = True

common_trails_file.close()

entry_counter = 0
all_trails_counts = {}
all_trails_titles = {}

for entry in dump.parse():
    title = entry.title
    print('entry #' + str(entry_counter) + ': ' + title)

    # Including only main space
    if entry.ns not in ('0'):
        continue

    # Before the space there is a ' ' char,
    # whatever that is
    trails = re.findall(
        r'\]\]([^0-9<*";:|\'.,=+({}?!/  \n\t)[\]-]+)',
        entry.text,
        re.UNICODE
    )

    for trail in trails:
        if trail in common_trails:
            continue

        if trail in all_trails_counts:
            all_trails_counts[trail] += 1
        else:
            all_trails_counts[trail] = 1
            all_trails_titles[trail] = {}

        all_trails_titles[trail][title] = True

    if args.stop_after and entry_counter == args.stop_after:
        break

    entry_counter += 1

trails_dirname = 'TRAILS_OUT'
if not os.path.isdir(trails_dirname):
    os.mkdir(trails_dirname)

single_trails_filename = trails_dirname + '/' + '_single_trails.txt'
single_trails_file = open(
    single_trails_filename,
    encoding='utf-8',
    mode='w'
)

problematic_trails_filename = trails_dirname + '/' + '_problematic_trails.txt'

trail_index = 0

for trail in sorted(all_trails_counts, key=all_trails_counts.get):
    trail_index += 1
    trail_index_str = str(trail_index)

    instance_count = all_trails_counts[trail]
    instance_count_line = 'Trail #' + trail_index_str + ' "' + trail
    instance_count_line += '" found ' + str(instance_count) + ' times'
    print(instance_count_line)

    if instance_count == 1:
        line = '* Trail "' + trail + '" found in [['
        line += list(all_trails_titles[trail])[0] + "]]\n"
        single_trails_file.write(line)

        continue

    trail_titles_filename = trails_dirname + '/' + 'trail_' + trail_index_str
    trail_titles_filename += '_' + trail + '_titles.txt'
    trail_titles_filename = replace_special_chars(trail_titles_filename)

    try:
        trail_titles_file = open(
            trail_titles_filename,
            encoding='utf-8',
            mode='w'
        )
    except IOError:
        with open(
            problematic_trails_filename,
            encoding='utf-8',
            mode='a'
        ) as problematic_trails_file:
            problematic_traile_line = 'problematic trail "' + trail + '"'
            problematic_trails_file.write(problematic_traile_line + "\n")
            problematic_trails_file.write("found in:\n")
            for title in all_trails_titles[trail]:
                problematic_trails_file.write(title + "\n")

        continue

    trail_titles_file.write(instance_count_line + "\n")

    for title in all_trails_titles[trail]:
        trail_titles_file.write('* [[' + title + ']]' + "\n")

    trail_titles_file.close()

single_trails_file.close()
