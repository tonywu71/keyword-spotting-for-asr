from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Optional
from kws.hit import Hit

from kws.query import Query


MAX_SECONDS_INTERVAL = 0.5


@dataclass(frozen=True)
class CTM_metadata():
    """
    Metadata of a word in a Conversation Time Marked (CTM) file
    Note:
    - tbeg = start time of the word in seconds
    - dur = duration of the word in seconds
    """
    file: str
    channel: int
    tbeg: float
    dur: float
    word: str
    score: float


def decode_ctm_line(ctm_line: str) -> CTM_metadata:
    try:
        file, channel, tbeg, dur, word, score = ctm_line.strip("\n").split()
        ctm_metadata = CTM_metadata(file, int(channel), float(tbeg), float(dur), word, float(score))
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

    
    def search(self, query: Query) -> Optional[Hit]:
        if query.is_word:
            if query.kwtext[0] in self.index:
                ctm_metadata = self.index[query.kwtext[0]][0]
                return Hit.from_ctm_metadata(ctm_metadata)
        else:
            pass
        
        raise NotImplementedError("Search method not implemented yet")
