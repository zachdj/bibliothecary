# ArXiv Bibliothecary

<h3 align="center">
Arxiv paper recommendations using SOTA language models.
</h3>

Bibliothecary is a library and software system that seeks to provide highly relevant paper recommendations
from the academic literature based on a user's criteria.
It is capable of recommending papers that may be of interest given the contents found in a
 collection of "seed" papers.
Bibliothecary is designed to aid in conducting literature reviews, exploring narrow academic topics, and 
curating a personalized feed of interesting papers.

Bibliothecary began as a project in [Zeta Global's](https://zetaglobal.com/) AI/ML 2020 Hackathon.

## Getting Started

### Acquiring ArXiv metadata

First you should download the [arXiv metadata dataset from Kaggle](https://www.kaggle.com/Cornell-University/arxiv).
This repository isn't much good without it.

Extract the file to the [data directory](./data) in this repository and rename `arxiv-metadata-oai-snapshot.json`
to `arxiv-metadata.json`.  Certain parts of this codebase may depend on this canonical name because I was in a 
big hurry and got very sloppy during development.

**TODO**: add script to download the file and unzip it in the right spot 

### Installation

This project uses [conda](https://docs.conda.io/en/latest/) to manage dependencies.  
Install conda, then run the following command to create a conda environment with this project's dependencies:

```shell script
conda env create --name arxiv -f environment.yml
```

Before running any of the scripts in this project, you should first activate the environment as follows:
```shell script
conda activate arxiv
```

### Generating Datasets

The `make_data_sample` script is intended to serve as a command-line utility for generating subsets of the arxiv 
data on demand.  
It generates a subset of the arxiv metadata filtered by [category](https://arxiv.org/category_taxonomy) and date.
The following commands describe a few usage examples.  
For full instructions, run `python scripts/make_data_sample.py --help`.

#### Sample dataset

This is a tiny subset of the arXiv metadata intended for development and sandboxing.
It includes 1000 entries (from any category) submitted in 2020

```shell script
python scripts/make_data_sample.py 1000 -y 2020 -o ./data/sample.json
```

#### 2018-2020 AI/ML Dataset

This dataset includes all papers between 2018 and 2020 from the following categories:
- cs.AI: Artificial Intelligence
- cs.CV: Computer Vision and Pattern Recognition
- cs.DC: Distributed Parallel and Cluster Computing
- cs.GT: Computer Science and Game Theory
- cs.LG: Machine Learning
- cs.MA: Multiagent Systems
- cs.NA: Numerical Analysis
- cs.NE: Neural and Evolutionary Computing
- cs.SC: Symbolic Computation
- math.NA: Numerical Analysis
- math.PR: Probability
- stat.CO: Computation
- stat.ML: Machine Learning

The idea was to curate a selection where the Zeta AI/ML team would be able to tell which papers 
were similar to others and should thus be recommended.  These categories and years were also selected
to reduce the size of the dataset and ensure reasonable computational times.

The total number of metadata entries in this dataset is 160,292.

```shell script
python scripts/make_data_sample.py 500000 -y 2018 2019 2020 -c cs.AI cs.CV cs.DC cs.GT cs.LG cs.MA cs.NA cs.NE cs.SC math.NA math.PR stat.CO stat.ML -o ./data/recent_aiml.json
```

## Authors

- [Zach Jones](https://github.com/zachdj)