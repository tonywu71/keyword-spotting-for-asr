from collections import defaultdict, namedtuple
from pathlib import Path
from typing import DefaultDict


MAX_SECONDS_INTERVAL = 0.5


# Note:
# - tbeg = start time of the word in seconds
# - dur = duration of the word in seconds
CTM_metadata = namedtuple("CTM_metadata", "file channel tbeg dur word score")


def decode_ctm_line(ctm_line: str) -> CTM_metadata:
    try:
        ctm_metadata = CTM_metadata(*ctm_line.strip("\n").split())
    except:
        raise ValueError(f"Error while generating index -> Invalid CTM line: {ctm_line}")
    return ctm_metadata


class Index:
    def __init__(self, ctm_filepath: str) -> None:
        self.ctm_filepath = Path(ctm_filepath)
        assert self.ctm_filepath.is_file(), f"CTM file not found: {ctm_filepath}"
        
        self.index = self._build_index()
        
    
    def _build_index(self) -> DefaultDict[str, list]:
        index = defaultdict(list)
        
        with self.ctm_filepath.open("r") as f:
            for ctm_line in f.readlines():
                ctm_metadata = decode_ctm_line(ctm_line)
                index[ctm_metadata.word].append(ctm_metadata)
        
        return index

    
    def search(self):
        raise NotImplementedError("Search method not implemented yet")
