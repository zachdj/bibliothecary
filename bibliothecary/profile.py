""" Creates a profile given a processing metadata file and a set of papers """

import argparse
import json
import numpy as np
import pathlib
import pickle
from transformers import pipeline

# TODO: need to move this logic to somewhere in utils
_working_dir = pathlib.Path(__file__).parent.parent


def load_data(paper_ids, dataset):
    processed_dataset_path = _working_dir / 'data' / 'processed' / f'{dataset}.json'
    # TODO: I wish there was a better way to extract only the entries from my list of ids
    target_ids = set(paper_ids)
    target_entries = []
    with open(str(processed_dataset_path), 'r') as f:
        current_line = f.readline()
        while len(current_line):
            entry = json.loads(current_line)
            if entry['id'] in target_ids:
                target_entries.append(entry)
            current_line = f.readline()

    return target_entries


def process_entries(entries, model, dim_reducer):
    language_model = pipeline('feature-extraction', model=model)
    embedded_entries = []
    for entry in entries:
        features = np.array(language_model(entry['processed_text']))
        if features.shape[0] > 1:
            features = features[0]

        features = features.squeeze()
        # mean vector will hopefully represent the whole paragraph
        mean_features = np.mean(features, axis=0)
        embedded_entries.append(mean_features)

    entries = np.stack(embedded_entries, axis=0)
    aggregate_entry = np.mean(entries, axis=0)
    print(aggregate_entry.shape)

    # run aggregate entry through dimensionality reduction model
    final_result = aggregate_entry
    if dim_reducer:
        with open(str(dim_reducer), 'rb') as f_in:
            dim_reducer_model = pickle.load(f_in)

        X = np.expand_dims(aggregate_entry, axis=0)
        final_result = dim_reducer_model.transform(X).squeeze()

    # this result is now ready to pass to our lookup tree
    print(final_result.shape)
    return final_result


if __name__ == '__main__':
    dataset = '2017_aiml_small'
    dim = 10
    model = 'distilbert-base-uncased'
    # paper_ids = [
    #     '1701.02369', # Reinforcement Learning based Embodied Agents Modelling Human Users Through Interaction and Multi-Sensory Perception
    #     '1701.02392', # Reinforcement Learning via Recurrent Convolutional Neural Networks
    #     '1701.07274',
    #     '1701.08810', # Reinforcement Learning Algorithm Selection
    #     '1701.08878', # Deep Reinforcement Learning for Robotic Manipulation-The state of the  art
    # ]
    # outfile = _working_dir / 'data' / 'profiles' / 'rl.npy'

    paper_ids = [
        '1701.02392',  # Reinforcement Learning via Recurrent Convolutional Neural Networks
        '1702.01721', # View Independent Vehicle Make, Model and Color Recognition Using Convolutional Neural Network
        '1702.06286', # Convolutional Recurrent Neural Networks for Polyphonic Sound Event  Detection
        '1702.07908', # CHAOS: A Parallelization Scheme for Training Convolutional Neural Networks
        '1703.00737', # Wireless Interference Identification with Convolutional Neural Networks
    ]
    outfile = _working_dir / 'data' / 'profiles' / 'cnn.npy'

    dim_reducer = str(_working_dir / 'data' / 'embeddings' / f'{dataset}_{model}_{dim}.reducer.pkl')
    entries = load_data(paper_ids, dataset)
    result = process_entries(entries, model, dim_reducer)
    np.save(str(outfile), result)

    print('Done')
