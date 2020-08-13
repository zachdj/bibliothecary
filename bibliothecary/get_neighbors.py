""" Builds the ball tree for kNN lookup """

import argparse
import json
import numpy as np
import pathlib
import pickle
from sklearn.neighbors import BallTree

# TODO: need to move this logic to somewhere in utils
_working_dir = pathlib.Path(__file__).parent.parent

if __name__ == '__main__':
    dataset = '2017_aiml_small'
    dim = 10
    model = 'distilbert-base-uncased'
    k = 30
    # profile = 'rl'
    profile = 'cnn'

    input_file = _working_dir / 'data' / 'embeddings' / f'{dataset}_{model}_{dim}.npy'
    profile_file = _working_dir / 'data' / 'profiles' / f'{profile}.npy'

    # load the input file
    X = np.load(str(input_file))
    print(X.shape)
    tree = BallTree(X)
    print('Done building tree')

    # get some neighbors
    profile = np.load(str(profile_file))
    print(profile)
    profile = profile.reshape(1, -1)  # reshape since tree expects a 2D array
    dist, indices = tree.query(profile, k=k)
    print('Query results:')
    print(indices)
    print(dist)

    # translate indices back into arXiv ids
    data_source = _working_dir / 'data' / 'processed' / f'{dataset}.json'
    fp = open(str(data_source))
    for i, line in enumerate(fp):
        if i in indices:
            entry = json.loads(line)
            print(f'Index {i} is arxiv id {entry["id"]}')
            print(f'\t with url: https://arxiv.org/abs/{entry["id"]}')

    print('DONE')