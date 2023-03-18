from pathlib import Path
from typing import Dict, List


def read_morph_dict(morph_filepath: str) -> Dict[str, List[str]]:
    assert Path(morph_filepath).is_file(), f"Morph file not found: {morph_filepath}"
    
    word_to_morphs = {}
    
    with open(morph_filepath, "r") as f:
        for line in f.readlines():
            word, morphs = line.strip().split(maxsplit=1)
            word_to_morphs[word] = morphs.split()
    
    return word_to_morphs
