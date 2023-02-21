from typing import DefaultDict, List, Optional

from pathlib import Path

from collections import defaultdict

import pandas as pd

from kws.hit import Hit
from kws.query import Query
from kws.kws_metadata import CTM_metadata


MAX_SECONDS_INTERVAL = 0.5


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

    
    def _aggregate_hits(self, list_hits: List[Hit]) -> Hit:
        assert list_hits, "list_hits is empty"
        file = list_hits[0].file
        channel = list_hits[0].channel
        
        def gen_from_list_hits():
            for hit in list_hits:
                yield hit.channel, hit.tbeg, hit.dur, hit.score
        
        df = pd.DataFrame(gen_from_list_hits(), columns=["channel", "tbeg", "dur", "score"])
        df_agg = df.agg({"tbeg": "min", "dur": "sum", "score": "prod"})
        
        return Hit(file=file, channel=channel, tbeg=df_agg["tbeg"], dur=df_agg["dur"], score=df_agg["score"])  # type: ignore
    
    
    def search(self, query: Query) -> Optional[List[Hit]]:
        if query.is_word:
            if query.kwtext[0] in self.index:
                ctm_metadata = self.index[query.kwtext[0]][0]
                return [Hit.from_ctm_metadata(ctm_metadata)]
            else:
                return None
        
        else:
            if query.kwtext[0] not in self.index:
                return None
            
            else:
                # TODO: Verify which elt of the list should be used (currently using the first one)
                # My guess is that we have to try all possible w2 knowing the previous w1 -> sort of tree traversal
                list_hits = [Hit.from_ctm_metadata(self.index[query.kwtext[0]][0])]
                for w1, w2 in zip(query.kwtext, query.kwtext[1:]):
                    if w1 not in self.index or w2 not in self.index:
                        return None
                    else:
                        ctm_metadata_1 = self.index[w1][0]
                        ctm_metadata_2 = self.index[w2][0]
                        if ctm_metadata_2.tbeg - ctm_metadata_1.tbeg <= MAX_SECONDS_INTERVAL:
                            list_hits.append(Hit.from_ctm_metadata(ctm_metadata_2))
                        break
                return list_hits
