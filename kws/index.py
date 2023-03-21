from typing import DefaultDict, List, Optional
from collections import deque

from pathlib import Path

from collections import defaultdict
from kws.grapheme_confusion.grapheme_confusion import GraphemeConfusions

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


def _get_posterior_metadata(ctm_metadata: CTM_metadata, posterior: float) -> CTM_metadata:
    ctm_posterior_metadata = CTM_metadata(file=ctm_metadata.file,
                                          channel=ctm_metadata.channel,
                                          tbeg=ctm_metadata.tbeg,
                                          dur=ctm_metadata.dur,
                                          word=ctm_metadata.word,
                                          score=ctm_metadata.score*posterior)
    return ctm_posterior_metadata


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
    
    
    def _iv_search(self, query: Query) -> List[HitSequence]:
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
                    if w2_hit.tbeg > w1_hit.tbeg and w2_hit.tbeg - (w1_hit.tbeg + w1_hit.dur) <= MAX_SECONDS_INTERVAL:  # allow overlap
                        hitseq_ = hitseq.copy()
                        hitseq_.append(w2_hit)
                        stack.append(hitseq_)
            else:
                pass
            
        return list_hitseqs
    
    
    def _oov_search(self,
                    query: Query,
                    grapheme_confusion: GraphemeConfusions) -> List[HitSequence]:
        
        list_hitseqs: List[HitSequence]= []
        stack = deque()
        
        # Initialize stack with first word:
        first_word = query.kwtext[0]
        
        for file in self.index.keys():
            
            if first_word in self.index[file]:
                for first_word_metadata in self.index[file][first_word]:
                    stack.append(HitSequence([Hit.from_ctm_metadata(first_word_metadata)]))  # TODO: Check if the appended object if correct
            
            else:  # If first word is OOV, we try to find it with grapheme confusion:
                closest_iv_word = grapheme_confusion.get_closest_iv_word(first_word)
                
                if closest_iv_word is None:
                    # Note: With the current implementation, this should never happen.
                    return list_hitseqs

                if closest_iv_word in self.index[file]:
                    posterior = grapheme_confusion._similarity_prob(first_word, closest_iv_word)
                    for first_word_metadata in self.index[file][closest_iv_word]:
                        first_word_metadata_posterior = _get_posterior_metadata(first_word_metadata, posterior)
                        stack.append(HitSequence([Hit.from_ctm_metadata(first_word_metadata_posterior)]))
        
        
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
                for first_word_metadata in self.index[current_file][w2]:
                    w2_hit = Hit.from_ctm_metadata(first_word_metadata)
                    if 0 < w2_hit.tbeg - w1_hit.tbeg <= MAX_SECONDS_INTERVAL:
                        hitseq_ = hitseq.copy()
                        hitseq_.append(w2_hit)
                        stack.append(hitseq_)
            
            else:
                closest_iv_word = grapheme_confusion.get_closest_iv_word(w2)
                
                if closest_iv_word is None:
                    # Note: With the current implementation, this should never happen.
                    continue
                
                posterior = grapheme_confusion._similarity_prob(w2, closest_iv_word)
                for first_word_metadata in self.index[current_file][closest_iv_word]:
                    w2_metadata_posterior = _get_posterior_metadata(first_word_metadata, posterior)
                    w2_hit = Hit.from_ctm_metadata(w2_metadata_posterior)
                    if 0 < w2_hit.tbeg - w1_hit.tbeg <= MAX_SECONDS_INTERVAL:
                        hitseq_ = hitseq.copy()
                        hitseq_.append(w2_hit)
                        stack.append(hitseq_)
        
        return list_hitseqs
    
    
    def search(self,
               query: Query,
               normalize_scores: bool=False,
               gamma: float=1.0,
               grapheme_confusion: Optional[GraphemeConfusions]=None) -> List[HitSequence]:
        
        if grapheme_confusion is None:
            list_hitseqs = self._iv_search(query)
        else:
            list_hitseqs = self._oov_search(query, grapheme_confusion=grapheme_confusion)
        
        if normalize_scores:
            for hitseq in list_hitseqs:
                hitseq.normalize_scores(gamma=gamma)
        
        return list_hitseqs
