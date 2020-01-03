#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import re
from pywikibot import xmlreader

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

args = argparser.parse_args()

dump = xmlreader.XmlDump(args.dump_filename)

common_trails = {}
common_trails_filename = 'common-trails.he.txt'
common_trails_file = open(
    common_trails_filename,
    encoding='utf-8',
    mode='r'
)

special_char_replacements = {
    u'\u200B': 'EXPLICITZEROWIDTHSPACE',
    u'\u200E': 'EXPLICITLRM',
    u'\u200F': 'EXPLICITRLM',
    u'\u202C': 'EXPLICITPDF',
    u'\u202D': 'EXPLICITLRO',
    u'\u202E': 'EXPLICITRLO',
}

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

trail_counter = 0

for trail in sorted(all_trails_counts, key=all_trails_counts.get):
    trail_counter += 1
    trail_counter_str = str(trail_counter)

    instance_count = all_trails_counts[trail]
    instance_count_line = 'Trail #' + trail_counter_str + ' "' + trail
    instance_count_line += '" found ' + str(instance_count) + ' times'
    print(instance_count_line)

    if instance_count == 1:
        line = '* Trail "' + trail + '" found in [['
        line += list(all_trails_titles[trail])[0] + "]]\n"
        single_trails_file.write(line)

        continue

    trail_titles_filename = trails_dirname + '/' + 'trail_' + trail_counter_str
    trail_titles_filename += '_' + trail + '_titles.txt'

    for special_char in special_char_replacements:
        trail_titles_filename = trail_titles_filename.replace(
            special_char,
            special_char_replacements[special_char]
        )

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
