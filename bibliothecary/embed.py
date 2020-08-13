""" Transform text from arXiv metadata into a feature vector """

# TODO: make this step in a CLI with configurable params

import argparse
import json
from multiprocessing import Process
import numpy as np
import pathlib
import pickle
from sklearn.random_projection import SparseRandomProjection
from transformers import pipeline


_working_dir = pathlib.Path(__file__).parent.parent

_models = [
    'bert-base-uncased',
    'openai-gpt',
    'gpt2',
    'ctrl',
    'transfo-xl-wt103',
    'xlnet-base-cased',
    'xlm-mlm-enfr-1024',
    'distilbert-base-uncased',
    'roberta-base',
    'xlm-roberta-base'
]

_default_model = _models[0]
_default_input_file = str(_working_dir / 'data' / 'processed' / 'sample.json')
_default_output_dir = _working_dir / 'data' / 'embeddings'


def process_entry(entry, model):
    # TODO: need to extract preprocessing steps to some reproducible pipeline
    print(f'working on entry {entry["id"]}')
    # assumes entry has been preprocessed to have a `processed_text` field
    text = entry['processed_text']
    features = np.array(model(text))
    if features.shape[0] > 1:
        features = features[0]

    features = features.squeeze()
    # mean vector will hopefully represent the whole paragraph
    mean_features = np.mean(features, axis=0)

    return mean_features


def process_file(file, model='distilbert-base-uncased', dim_reduction='auto', output_path=None):
    # establish conventional file names for output
    save_dir = pathlib.Path(output_path) if output_path else _default_output_dir
    vec_outpath = save_dir / f'{pathlib.Path(file).stem}_{model}_{dim_reduction}.npy'
    dim_reducer_outpath = save_dir / f'{pathlib.Path(file).stem}_{model}_{dim_reduction}.reducer.pkl'
    metadata_outpath = save_dir / f'{pathlib.Path(file).stem}_{model}_{dim_reduction}.metadata.json'

    # keep track of config
    metadata = {
        'model': model,
        'source_file': file,
        'embeddings_file': str(vec_outpath),  # filled in later
        'dim_reduction': dim_reduction,
        'dim_reduction_transformer_file': str(dim_reducer_outpath) if dim_reduction else None
    }

    language_model = pipeline(task='feature-extraction', model=model)

    embedded_entries = []
    with open(file, 'r') as f:
        current_line = f.readline()
        while len(current_line):
            entry = process_entry(json.loads(current_line), language_model)
            embedded_entries.append(entry)
            current_line = f.readline()

    entries_vec = np.stack(embedded_entries, axis=0)
    print(f'Processed {len(embedded_entries)} from file {file}')

    dim_reducer = None
    if dim_reduction is not None:
        dim_reducer = SparseRandomProjection(n_components=dim_reduction)
        dim_reducer.fit(entries_vec)
        entries_vec = dim_reducer.transform(entries_vec)

        # save trained dim reducer
        with open(str(dim_reducer_outpath), 'wb') as f_out:
            pickle.dump(dim_reducer, f_out)

    # save embeddings
    np.save(vec_outpath, entries_vec)

    # save metadata
    with open(str(metadata_outpath), 'w') as f_out:
        json.dump(metadata, f_out)


if __name__ == '__main__':
    # infile = _working_dir / 'data' / 'processed' / 'sample.json'
    # infile = _working_dir / 'data' / 'processed' / '2017_aiml_small.json'
    infile = _working_dir / 'data' / 'processed' / 'recent_aiml.json'
    dims = [10, 5]
    # trial_models = ['bert-base-uncased', 'distilbert-base-uncased']
    trial_models = ['distilbert-base-uncased']
    processes = []
    for m in trial_models:
        for dim in dims:
            p = Process(target=process_file, args=(str(infile), m, dim))
            processes.append(p)
            p.start()

    for p in processes:
        p.join()
