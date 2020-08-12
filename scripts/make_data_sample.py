""" Create data sample

This script creates a sample of the first N entries from the `data/arxiv-metadata.json` file.  It optionally filters
the file by category and year.

Run python scripts/make_data_sample.py --help for usage instructions.

"""

import argparse
import json
import pathlib
import sys

# make sure bibliothecary module is available to this script
src_dir = str(pathlib.Path(__file__).parent.parent.resolve())
try:
    sys.path.index(src_dir)
except ValueError:
    sys.path.append(src_dir)

import bibliothecary.util.categories as arxiv_categories
import bibliothecary.util.arxiv as arvix_utils

DATA_PATH = (pathlib.Path(__file__).parent.parent / 'data/arxiv-metadata.json').resolve().__str__()
SUPER_CATEGORIES = arxiv_categories.super_categories()


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Utility script to make sample data from arxiv metadata")
    parser.add_argument('n', type=int, default=1000, help='Total number of entries to include in the sample')
    parser.add_argument('--years', '-y', type=int, nargs='*', default=[],
                        help='Filter entries which were not submitted during these years. '
                             'Includes all years by default')
    parser.add_argument('--categories', '-c', nargs='*', default=[],
                        help='Filter entries which do not belong to these categories. '
                             'Supports both super- and sub-categories. '
                             'Includes all categories by default.')
    parser.add_argument('--output', '-o', default='../data/sample.json',
                        help='File where the sample will be written')

    args = parser.parse_args(argv)
    return vars(args)


def make_sample(args):
    entries = []

    limit = args['n']
    filter_by_year = len(args['years']) > 0
    allowed_years = args['years']
    filter_by_category = len(args['categories']) > 0
    allowed_categories = set(
        arxiv_categories.sub_categories(*args['categories']).keys()
    )

    print(f'Creating sample of size {limit}')
    print('\tFrom any year' if not filter_by_year else f'\tFrom years: {allowed_years}')
    print('\tFrom all categories' if not filter_by_category else f'\tFrom categories: {allowed_categories}')

    with open(DATA_PATH, 'r') as f:
        # each line in the file is an arvix metadata entry
        current_line = f.readline()
        while len(current_line) and len(entries) < limit:
            entry = json.loads(current_line)
            date_metadata = arvix_utils.parse_arxiv_id(entry['id'])
            if filter_by_year and date_metadata['year'] not in allowed_years:
                # print(f'skipping entry {entry["id"]} due to mismatched year') # TODO: would be nice to have this as a logging stmt
                current_line = f.readline()
                continue

            categories = set(entry['categories'][0].split())
            if filter_by_category and categories.isdisjoint(allowed_categories):
                # print(f'skipping entry {entry["id"]} due to mismatched categories') # TODO: would be nice to have this as a logging stmt
                current_line = f.readline()
                continue

            # print(f'Including entry {entry["id"]}') # TODO: would be nice to have this as a logging stmt
            entries.append(entry)
            current_line = f.readline()

    # the format of the output file matches that of the input file: one JSON-encoded entry per line
    print(f'Writing {len(entries)} entries to {args["output"]}')
    with open(args['output'], 'w') as outfile:
        for entry in entries:
            outfile.write(json.dumps(entry) + '\n')


if __name__ == '__main__':
    arg_dict = parse_args(sys.argv[1:])
    make_sample(arg_dict)
