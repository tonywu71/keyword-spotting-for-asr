from typing import Optional, Set
from kws.grapheme_confusion.utils import get_iv_set, load_grapheme_confusion


SIL_TOKEN = "sil"


class GraphemeConfusionBase:
    """
    Base class for grapheme confusion models.
    Assumes that all cost functions are unit cost.
    """
    
    def _levenshtein_distance(self, word1: str, word2: str) -> float:
        """Compute Levenshtein distance between two words."""
        n1 = len(word1)
        n2 = len(word2)

        # Use backtracking to compute Levenshtein distance:
        cache = {}
        
        def helper(p1, p2) -> int:
            # --- CACHING ---
            if (p1, p2) in cache:
                return cache[(p1, p2)]
            
            # --- MAIN ---
            if p1 == n1:
                total_insertion_cost = 0
                for char in word2[p2:]:
                    total_insertion_cost += self._insertion_cost(char)
                cache[(p1, p2)] = total_insertion_cost
                return cache[(p1, p2)]
            elif p2 == n2:
                total_insertion_cost = 0
                for char in word1[p1:]:
                    total_insertion_cost += self._deletion_cost(char)
                cache[(p1, p2)] = total_insertion_cost
                return cache[(p1, p2)]
            
            else:
                if word1[p1] == word2[p2]:
                    cache[(p1, p2)] = helper(p1+1, p2+1)
                    return cache[(p1, p2)]
                else:
                    cache[(p1, p2)] = min(
                        helper(p1+1, p2) + self._deletion_cost(word1[p1]),
                        helper(p1, p2+1) + self._insertion_cost(word2[p2]),
                        helper(p1+1, p2+1) + self._substitution_cost(word1[p1], word2[p2])
                    )
                    return cache[(p1, p2)]
        
        return helper(p1=0, p2=0)
    
    
    def _insertion_cost(self, char: str) -> float:
        """Unit cost for insertion of a character"""
        return 1.0
    
    
    def _deletion_cost(self, char: str) -> float:
        """Unit cost for deletion of a character"""
        return 1.0
    
    
    def _substitution_cost(self, char_1: str, char_2: str) -> float:
        """Unit cost for substitution of a character"""
        return 1.0


class GraphemeConfusion(GraphemeConfusionBase):
    def __init__(self,
                 grapheme_confusion_filepath: str,
                 ctm_filepath: str):
        super().__init__()
        self.confusion_dict = load_grapheme_confusion(grapheme_confusion_filepath)
        self.iv_set = get_iv_set(ctm_filepath)
    
    
    def is_iv_word(self, word: str) -> bool:
        return word in self.iv_set

    
    def get_closest_iv_word(self, oov_word: str, subset: Optional[Set[str]]=None) -> Optional[str]:
        if subset is not None:
            iv_set = self.iv_set.intersection(subset)
        else:
            iv_set = self.iv_set
        
        min_dist_iv_word = None
        min_dist = float("inf")
        for iv_word in iv_set:
            dist = self._levenshtein_distance(oov_word, iv_word)
            if dist < min_dist:
                min_dist = dist
                min_dist_iv_word = iv_word
        return min_dist_iv_word
    
    
    def _similarity_score(self, s0: str, s1: str) -> float:
        max_length = max(len(s0), len(s1))
        if max_length == 0:
            return 0.0
        return 1.0 - self._levenshtein_distance(s0, s1) / max_length
    
    
    # --------- COST FUNCTIONS ---------
    # We override the default cost functions with the ones from the grapheme confusion matrix.
    def _insertion_cost(self, char: str) -> float:
        return 1 - self.confusion_dict[SIL_TOKEN][char]
    
    
    def _deletion_cost(self, char: str) -> float:
        return 1 - self.confusion_dict[char][SIL_TOKEN]
    
    
    def _substitution_cost(self, char_1: str, char_2: str) -> float:
        return 1 - self.confusion_dict[char_1][char_2]
