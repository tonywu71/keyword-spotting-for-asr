from typing import DefaultDict, Deque, Dict, List, Optional
from collections import deque

from pathlib import Path

from collections import defaultdict
from kws.grapheme_confusion.grapheme_confusion import GraphemeConfusion

from kws.hit import Hit, HitSequence, normalize_scores_hitseqs
from kws.query import Query
from kws.kws_metadata import CTM_metadata

from kws.constants import MAX_SECONDS_INTERVAL


def preprocess_word(data: str):
    return data.lower()


def decode_ctm_line(ctm_line: str, next_word: Optional[str]=None) -> CTM_metadata:
# try:
    file, channel, tbeg, dur, word, score = ctm_line.strip("\n").split()
    word = preprocess_word(word)
    ctm_metadata = CTM_metadata(file, int(channel), float(tbeg), float(dur), word, float(score), next_word=next_word)
    # except:
    #     raise ValueError(f"Error while generating index -> Invalid CTM line: {ctm_line}")
    return ctm_metadata


def _get_posterior_metadata(ctm_metadata: CTM_metadata, posterior: float) -> CTM_metadata:
    ctm_posterior_metadata = CTM_metadata(file=ctm_metadata.file,
                                          channel=ctm_metadata.channel,
                                          tbeg=ctm_metadata.tbeg,
                                          dur=ctm_metadata.dur,
                                          word=ctm_metadata.word,
                                          score=ctm_metadata.score*posterior,
                                          next_word=ctm_metadata.next_word)
    return ctm_posterior_metadata


class Index:
    def __init__(self, ctm_filepath: str) -> None:
        self.ctm_filepath = Path(ctm_filepath)
        assert self.ctm_filepath.is_file(), f"CTM file not found: {ctm_filepath}"
        
        self.index = self._build_index()
        
    
    def _build_index(self) -> DefaultDict[str, DefaultDict[str, List[CTM_metadata]]]:
        index = defaultdict(lambda: defaultdict(list))
        
        with self.ctm_filepath.open("r") as f:
            lines = f.readlines()
            for ctm_line, next_ctm_line in zip(lines, lines[1:]):
                next_ctm_metadata = decode_ctm_line(next_ctm_line)
                ctm_metadata = decode_ctm_line(ctm_line, next_word=next_ctm_metadata.word)
                index[ctm_metadata.file][ctm_metadata.word].append(ctm_metadata)
        
        return index
    
    
    def _search(self, query: Query) -> List[HitSequence]:
        """
        Search for a query in the index.
        """
        
        list_hitseqs: List[HitSequence] = []
        stack: Deque[HitSequence] = deque()
        
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
            
            if w2 == w1_hit.next_word_in_ctm:  # Note: This condition implies (w2 in self.index[current_file]) but the reciprocal is not necessarily true.
                for w2_metadata in self.index[current_file][w2]:
                    w2_hit = Hit.from_ctm_metadata(w2_metadata)
                    if w2_hit.tbeg >= w1_hit.tbeg and w2_hit.tbeg - (w1_hit.tbeg + w1_hit.dur) <= MAX_SECONDS_INTERVAL:  # allow overlap
                        hitseq_ = hitseq.copy()
                        hitseq_.append(w2_hit)
                        stack.append(hitseq_)
            else:
                pass
            
        return list_hitseqs
    
    
    def _search_gc(self,
                   query: Query,
                   grapheme_confusion: GraphemeConfusion) -> List[HitSequence]:
        """
        Search for a query in the index with grapheme confusion.
        """
        
        list_hitseqs: List[HitSequence]= []
        stack: Deque[HitSequence] = deque()
        
        # Wrap grapheme_confusion.get_closest_iv_word to implement caching in order speed up search:
        cache: DefaultDict[str, Dict[str, Optional[str]]] = defaultdict(dict)
        def get_closest_iv_word(word: str, file: str) -> Optional[str]:
            if file not in cache or word not in cache[file]:
                cache[file][word] = grapheme_confusion.get_closest_iv_word(oov_word=word, subset=set(self.index[file].keys()))
            return cache[file][word]
        
        
        # Initialize stack with first word:
        first_word = query.kwtext[0]
        
        for file in self.index.keys():
            if first_word in self.index[file]:
                for first_word_metadata in self.index[file][first_word]:
                    stack.append(HitSequence([Hit.from_ctm_metadata(first_word_metadata)]))
            
            else:  # If first word is OOV, we try to find it with grapheme confusion:
                closest_iv_word = get_closest_iv_word(first_word, file)
                
                if closest_iv_word is None:
                    continue  # If we cannot find a closest IV word, we skip this file.
                
                if closest_iv_word in self.index[file]:
                    posterior = grapheme_confusion._similarity_score(first_word, closest_iv_word)
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
            
            if w2 == w1_hit.next_word_in_ctm:  # Note: This condition implies (w2 in self.index[current_file]) but the reciprocal is not necessarily true.
                for w2_metadata in self.index[current_file][w2]:
                    w2_hit = Hit.from_ctm_metadata(w2_metadata)
                    if w2_hit.tbeg >= w1_hit.tbeg and w2_hit.tbeg - (w1_hit.tbeg + w1_hit.dur) <= MAX_SECONDS_INTERVAL:  # allow overlap
                        hitseq_ = hitseq.copy()
                        hitseq_.append(w2_hit)
                        stack.append(hitseq_)
            
            else:
                # If w2 is OOV, we try to find it with grapheme confusion:
                closest_iv_word = get_closest_iv_word(w2, current_file)
                
                if closest_iv_word is None or closest_iv_word != w1_hit.next_word_in_ctm:
                    continue  # If we cannot find a closest IV word OR if the closest IV word is not the next word in the query at hand, skip.
                
                else:  # Note: Necessarily we have closest_iv_word in self.index[current_file]
                    posterior = grapheme_confusion._similarity_score(w2, closest_iv_word)
                    for w2_metadata in self.index[current_file][closest_iv_word]:
                        w2_metadata_posterior = _get_posterior_metadata(w2_metadata, posterior=posterior)
                        w2_hit = Hit.from_ctm_metadata(w2_metadata_posterior)
                        if w2_hit.tbeg >= w1_hit.tbeg and w2_hit.tbeg - (w1_hit.tbeg + w1_hit.dur) <= MAX_SECONDS_INTERVAL:  # allow overlap
                            hitseq_ = hitseq.copy()
                            hitseq_.append(w2_hit)
                            stack.append(hitseq_)
        
        return list_hitseqs
    
    
    def search(self,
               query: Query,
               normalize_scores: bool=False,
               gamma: float=1.0,
               grapheme_confusion: Optional[GraphemeConfusion]=None) -> List[HitSequence]:
        
        if grapheme_confusion is None:
            list_hitseqs = self._search(query)
        else:
            list_hitseqs = self._search_gc(query, grapheme_confusion=grapheme_confusion)
        
        if normalize_scores:
            normalize_scores_hitseqs(list_hitseqs=list_hitseqs, gamma=gamma)
        
        return list_hitseqs
