from typing import Optional
from kws.grapheme_confusion.utils import get_iv_set, load_grapheme_confusion


class GraphemeConfusions:
    def __init__(self,
                 grapheme_confusion_filepath: str,
                 ctm_filepath: str,
                 min_dist: int = DEFAULT_MIN_DIST):
        self.confusion_dict = load_grapheme_confusion(grapheme_confusion_filepath)
        self.iv_set = get_iv_set(ctm_filepath)
    
    
    def is_iv_word(self, word: str) -> bool:
        return word in self.iv_set

    
    def closest_iv_word(self, oov_word) -> Optional[str]:
        min_dist_iv_word = None
        min_dist = float("inf")
        for iv_word in self.iv_set:
            dist = self._weighted_lev_distance(oov_word, iv_word)
            if dist < min_dist:
                min_dist = dist
                min_dist_iv_word = iv_word
        return min_dist_iv_word
    
    
    def _weighted_lev_distance(self, s0: str, s1: str) -> float:
        if s0 == s1:
            return 0.0

        v0, v1 = [0.0] * (len(s1) + 1), [0.0] * (len(s1) + 1)

        v0[0] = 0
        for i in range(1, len(v0)):
            v0[i] = v0[i - 1] + self._insertion_cost_fn(s1[i - 1])

        for i in range(len(s0)):
            s0i = s0[i]
            deletion_cost = self._deletion_cost_fn(s0i)
            v1[0] = v0[0] + deletion_cost

            for j in range(len(s1)):
                s1j = s1[j]
                cost = 0
                if s0i != s1j:
                    cost = self._substitution_cost_fn(s0i, s1j)
                insertion_cost = self._insertion_cost_fn(s1j)
                v1[j + 1] = min(
                    v1[j] + insertion_cost, v0[j + 1] + deletion_cost, v0[j] + cost
                )
            v0, v1 = v1, v0

        return v0[len(s1)]
    
    
    def _similarity_prob(self, s0: str, s1: str) -> float:
        m_len = max(len(s0), len(s1))
        if m_len == 0:
            return 0.0
        return 1.0 - self._weighted_lev_distance(s0, s1) / m_len

    
    def _insertion_cost_fn(self, char: str) -> float:
        return 1 - self.confusion_dict["sil"][char]

    
    def _deletion_cost_fn(self, char: str) -> float:
        return 1 - self.confusion_dict[char]["sil"]
    
    
    def _substitution_cost_fn(self, char_a: str, char_b: str) -> float:
        return 1 - self.confusion_dict[char_a][char_b]
