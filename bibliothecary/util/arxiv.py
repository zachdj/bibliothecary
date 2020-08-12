""" Utilities for parsing arXiv metadata """

import regex


def parse_arxiv_id(arxiv_id):
    """ Parses an arXiv submission id, extracting the submission date and number

    See https://arxiv.org/help/arxiv_identifier for info on id format
    """
    # ids like "math.GT/0309136"
    pre_2007_patten = regex.compile(r'\w+\-?\w+(\.\w+)?/\d+')
    # ids like "arXiv:0706.0001" or "arXiv:0706.1234v2" or just "0706.0001"
    modern_pattern = regex.compile(r'(arXiv:)?\d+\.\d+(v\d+)?')

    if pre_2007_patten.match(arxiv_id):
        # strip the subject class
        _id = arxiv_id[-7:]  # last 7 characters are YYmmNNN
        return {
            'year': 2000 + int(_id[:2]),  # first 2 chars are YY
            'month': int(_id[2: 4]),  # middle 2 chars are MM
            'number': int(_id[-3:])  # last 3 characters are the number
        }
    elif modern_pattern.match(arxiv_id):
        # strip arXiv: prefix if present
        _id = arxiv_id.replace('arXiv:', '')
        # strip version number if present
        if 'v' in _id:
            _id = _id[:_id.index('v')]
        yymm, number = _id.split('.')
        return {
            'year': 2000 + int(yymm[:2]),
            'month': int(yymm[-2:]),
            'number': int(number)
        }
    else:
        print(f'ERROR: could not parse arxiv id "{arxiv_id}"')
        return {
            'year': None,
            'month': None,
            'number': None
        }
