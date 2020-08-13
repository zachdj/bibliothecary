""" Preprocess abstracts and titles of arXiv metadata entries """

import argparse
import json
import pathlib
import re


_tex_command_pattern = r'\\\\\w+\{.*\}'
_tex_math_pattern = r'$.+$'

_stopword_file = str(pathlib.Path(__file__).parent.parent / 'data' / 'stopwords.txt')
with open(_stopword_file, 'r') as f:
    _stopwords = set([line.strip() for line in f.readlines()])


def process_entry(entry):
    new_entry = dict(entry)
    new_entry['processed_text'] = process_text(new_entry['title']) + ' ' + process_text(new_entry['abstract'])
    del new_entry['title']
    del new_entry['abstract']
    return new_entry


def process_text(text, remove_stopwords=False):
    """ Removes  special characters, escaped characters, and LaTeX commands from a chunk of text """
    # replace `\n` with whitespace
    text = text.replace(r'\n', ' ')
    # replace tex commands and equations
    text = re.sub(_tex_command_pattern, ' ', text)
    text = re.sub(_tex_math_pattern, ' ', text)
    # replace special characters
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)

    # lowercase everything
    text = text.lower()

    # remove single characters
    text = re.sub(r'\s\w\s', ' ', text)

    # replace multiple whitespace with just one
    text = re.sub(r'\s+', ' ', text)

    # remove stopwords
    if remove_stopwords:
        text = ' '.join([word for word in text.split() if word not in _stopwords])

    return text


def main():
    # TODO: make CLI for this preprocessing task
    infile = 'C:/Users/zach/Develop/bibliothecary/data/2018_ml_small.json'
    outfile = 'C:/Users/zach/Develop/bibliothecary/data/processed/2018_ml_small.json'

    with open(infile, 'r') as f_in:
        with open(outfile, 'w') as f_out:
            current_line = f_in.readline()
            while len(current_line):
                entry = json.loads(current_line)
                proc_entry = process_entry(entry)
                f_out.write(json.dumps(proc_entry) + '\n')
                current_line = f_in.readline()

    print('Done')


if __name__ == '__main__':
    main()
