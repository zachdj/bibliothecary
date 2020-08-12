# ArXiv Bibliothecary
Arxiv paper recommendations using SOTA language models


## Getting Started

### Generating Datasets

#### Sample dataset

This is a tiny subset of the arXiv metadata intended for development and sandboxing.
It includes 1000 entries (from any category) submitted in 2020

```shell script
python scripts/make_data_sample.py 1000 -y 2020 -o ./data/sample.json
```

#### Dataset used in 2020 hackathon

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
