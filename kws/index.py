from typing import DefaultDict, List, Tuple
from collections import deque

from pathlib import Path

from collections import defaultdict

from kws.hit import Hit, HitSequence
from kws.query import Query
from kws.kws_metadata import CTM_metadata

from kws.constants import MAX_SECONDS_INTERVAL


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
        
    
    def _build_index(self) -> DefaultDict[str, List[CTM_metadata]]:
        index = defaultdict(list)
        
        with self.ctm_filepath.open("r") as f:
            for ctm_line in f.readlines():
                ctm_metadata = decode_ctm_line(ctm_line)
                index[ctm_metadata.word].append(ctm_metadata)
        
        return index
    
    
    def search(self, query: Query) -> List[HitSequence]:
        list_hitseqs = []
        stack = deque()
        
        # Initialize stack with first word:
        for first_word_metadata in self.index[query.kwtext[0]]:
            stack.append(HitSequence([Hit.from_ctm_metadata(first_word_metadata)]))
        
        while stack:
            hitseq = stack.pop()
            next_idx = len(hitseq)
            
            # If we have a hit sequence:
            if next_idx >= len(query.kwtext):
                list_hitseqs.append(hitseq)
                continue
            
            # Otherwise, we continue to build the current hit sequence:
            w1_hit = hitseq[-1]
            w2 = query.kwtext[next_idx]
            if w2 in self.index:
                for w2_metadata in self.index[w2]:
                    w2_hit = Hit.from_ctm_metadata(w2_metadata)
                    if w2_hit.file == w1_hit.file:  # TODO: Re-index by file to increase speed
                        # if w1_hit.tbeg + w1_hit.dur <= w2_hit.tbeg <= w1_hit.tbeg + w1_hit.dur - MAX_SECONDS_INTERVAL:  # TODO: Allow overlaps?
                        if 0 < w2_hit.tbeg - w1_hit.tbeg <= MAX_SECONDS_INTERVAL:
                            hitseq.append(w2_hit)
                            stack.append(hitseq)
            else:
                pass
        
        return list_hitseqs
