from typing import Optional, Set
from kws.grapheme_confusion.utils import get_iv_set, load_grapheme_confusion


SIL_TOKEN = "sil"


class GraphemeConfusionBase:
    """
    Base class for grapheme confusion models.
    Assumes that all cost functions are unit cost.
    """
    
    def _levenshtein_distance(self, s0: str, s1: str) -> float:
        """Computes the weighted Levenshtein distance between two strings.
        Cf https://en.wikipedia.org/wiki/Levenshtein_distance"""
        # --------- EDGE CASE ---------
        if s0 == s1:
            return 0.

        # --------- MAIN ---------
        v0 = [0. for _ in range(len(s1)+1)]
        v1 = [0. for _ in range(len(s1)+1)]

        v0[0] = 0
        for i in range(1, len(v0)):
            v0[i] = v0[i - 1] + self._insertion_cost(s1[i - 1])

        for i in range(len(s0)):
            s0i = s0[i]
            deletion_cost = self._deletion_cost(s0i)
            v1[0] = v0[0] + deletion_cost

            for j in range(len(s1)):
                s1j = s1[j]
                cost = 0
                if s0i != s1j:
                    cost = self._substitution_cost(s0i, s1j)
                insertion_cost = self._insertion_cost(s1j)
                v1[j + 1] = min(
                    v1[j] + insertion_cost, v0[j + 1] + deletion_cost, v0[j] + cost
                )
            v0, v1 = v1, v0

        return v0[len(s1)]
    
    
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
