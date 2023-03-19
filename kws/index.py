from typing import DefaultDict, List
from collections import deque

from pathlib import Path

from collections import defaultdict

from kws.hit import Hit, HitSequence
from kws.query import Query
from kws.kws_metadata import CTM_metadata

from kws.constants import MAX_SECONDS_INTERVAL


def preprocess_word(data: str):
    return data.lower()


def decode_ctm_line(ctm_line: str) -> CTM_metadata:
    try:
        file, channel, tbeg, dur, word, score = ctm_line.strip("\n").split()
        word = preprocess_word(word)
        ctm_metadata = CTM_metadata(file, int(channel), float(tbeg), float(dur), word, float(score))
    except:
        raise ValueError(f"Error while generating index -> Invalid CTM line: {ctm_line}")
    return ctm_metadata


class Index:
    def __init__(self, ctm_filepath: str) -> None:
        self.ctm_filepath = Path(ctm_filepath)
        assert self.ctm_filepath.is_file(), f"CTM file not found: {ctm_filepath}"
        
        self.index = self._build_index()
        
    
    def _build_index(self) -> DefaultDict[str, DefaultDict[str, List[CTM_metadata]]]:
        index = defaultdict(lambda: defaultdict(list))
        
        with self.ctm_filepath.open("r") as f:
            for ctm_line in f.readlines():
                ctm_metadata = decode_ctm_line(ctm_line)
                index[ctm_metadata.file][ctm_metadata.word].append(ctm_metadata)
        
        return index
    
    
    def search(self,
               query: Query,
               normalize_scores: bool=False,
               gamma: float=1.0) -> List[HitSequence]:
        list_hitseqs: List[HitSequence] = []
        stack = deque()
        
        # Initialize stack with first word:
        first_word = query.kwtext[0]
        for file in self.index.keys():
            if first_word in self.index[file]:
                for first_word_metadata in self.index[file][first_word]:
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
            current_file = w1_hit.file
            w2 = query.kwtext[next_idx]
            
            if w2 in self.index[current_file]:
                for w2_metadata in self.index[current_file][w2]:
                    w2_hit = Hit.from_ctm_metadata(w2_metadata)
                    if 0 < w2_hit.tbeg - w1_hit.tbeg <= MAX_SECONDS_INTERVAL:
                        hitseq_ = hitseq.copy()
                        hitseq_.append(w2_hit)
                        stack.append(hitseq_)
            else:
                pass
        
        if normalize_scores:
            for hitseq in list_hitseqs:
                hitseq.normalize_scores(gamma=gamma)
        
        return list_hitseqs
