from __future__ import annotations
from typing import Iterator, List

import pandas as pd

from kws.kws_metadata import CTM_metadata

from kws.constants import MAX_SECONDS_INTERVAL


class Hit:
    def __init__(self, file: str, channel: int, tbeg: float, dur: float, word: str, score: float):
        self.file = file
        self.channel = channel
        self.tbeg = tbeg
        self.dur = dur
        self.word = word
        self.score = score

    
    @classmethod
    def from_ctm_metadata(cls, ctm_metadata: CTM_metadata):
        """Create a Hit from a CTM_metadata object"""
        return cls(file=ctm_metadata.file,
                   channel=ctm_metadata.channel,
                   tbeg=ctm_metadata.tbeg,
                   dur=ctm_metadata.dur,
                   word=ctm_metadata.word,
                   score=ctm_metadata.score)

    
    def __str__(self):
        return (f"Hit(file={self.file}, channel={self.channel}, "
                f"tbeg={self.tbeg}, dur={self.dur}, word={self.word}, "
                f"score={self.score})")
    
    
    def __repr__(self):
        return self.__str__()
        
    
    def overlaps_with(self, hit_2: Hit) -> bool:
        start1, start2 = self.tbeg, hit_2.tbeg
        end1, end2 = start1 + self.dur, start2 + hit_2.dur
        return (start1 <= end2) and (start2 <= end1)


class HitSequence:
    def __init__(self, hits: List[Hit]):
        self.hits = hits
        self._aggregate_hits_init()


    def _aggregate_hits_init(self) -> None:
        assert self.hits, "self.hits is empty"
        self.file = self.hits[0].file
        self.channel = self.hits[0].channel
        
        def gen_from_list_hits():
            for hit in self.hits:
                yield hit.channel, hit.tbeg, hit.dur, hit.word, hit.score
        
        df = pd.DataFrame(gen_from_list_hits(), columns=["channel", "tbeg", "dur", "word", "score"])
        df_agg = df.agg({"tbeg": "min", "dur": "sum", "score": "prod"})
        
        self.tbeg = df_agg["tbeg"]
        self.dur = df_agg["dur"]
        self.words = df["word"].str.cat(sep=" ").split()
        self.score = df_agg["score"]
    

    def __len__(self) -> int:
        return len(self.hits)
    
    
    def __getitem__(self, index: int) -> Hit:
        return self.hits[index]
    
    
    def __contains__(self, hit: Hit) -> bool:
        return hit in self.hits
    
    
    def __iter__(self) -> Iterator[Hit]:
        return iter(self.hits)
    
    
    def __next__(self) -> Hit:
        return next(iter(self.hits))


    def append(self, hit: Hit) -> None:
        assert hit.file == self.file, "Cannot append a hit from another file"
        assert hit.channel == self.channel, "Cannot append a hit from another channel"
        # assert hit.tbeg >= self.tbeg + self.dur, "Cannot append a hit that overlaps with the current sequence"  # TODO: Allow overlaps?
        # assert hit.tbeg <= self.tbeg + self.dur + MAX_SECONDS_INTERVAL, "Cannot append a hit that is too far from the current sequence"  # TODO: Check assert
        
        self.hits.append(hit)
        self.dur += hit.dur
        self.words += [hit.word]
        self.score *= hit.score
    
    
    def is_valid(self) -> bool:
        for hit_1, hit_2 in zip(self.hits, self.hits[1:]):
            if hit_2.tbeg - hit_1.tbeg <= MAX_SECONDS_INTERVAL:
                return False
        return True
