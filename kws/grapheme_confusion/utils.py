from collections import defaultdict
from pathlib import Path
from typing import DefaultDict
from copy import deepcopy
from toolz import valmap


def normalize_grapheme_confusion_dict(grapheme_confusion_dict: DefaultDict[str, DefaultDict[str, float]]) \
        -> DefaultDict[str, DefaultDict[str, float]]:
    grapheme_confusion_dict = deepcopy(grapheme_confusion_dict)
    
    for c1 in grapheme_confusion_dict:
        total = sum(grapheme_confusion_dict[c1].values())
        grapheme_confusion_dict[c1] = valmap(lambda x: x / total, grapheme_confusion_dict[c1])  # type: ignore
    
    return grapheme_confusion_dict


def load_grapheme_confusion(grapheme_confusion_filepath: str) \
        -> DefaultDict[str, DefaultDict[str, float]]:
    assert Path(grapheme_confusion_filepath).is_file(), f"Grapheme confusion file not found: {grapheme_confusion_filepath}"
    
    grapheme_confusion_dict: DefaultDict[str, DefaultDict[str, float]] = defaultdict(lambda: defaultdict(float))
    
    with open(grapheme_confusion_filepath, "r") as f:
        for line in f.readlines():
            graph_1, graph_2, count = line.strip().split()
            grapheme_confusion_dict[graph_1][graph_2] = float(count)
    
    grapheme_confusion_dict = normalize_grapheme_confusion_dict(grapheme_confusion_dict)
    
    return grapheme_confusion_dict
