from dataclasses import dataclass
from typing import List

@dataclass()
class DetectedKW():
    """
    Metadata of a HitSequence found and stored in the XML file output by the
    Index search (see <kw> element)
    """
    file: str
    channel: int
    tbeg: float
    dur: float
    score: float
    decision: bool
    
    def overlap(self, other: 'DetectedKW') -> bool:
        """
        Check if two DetectedKW objects overlap in time
        """
        return self.file == other.file and self.channel == other.channel and self.tbeg < other.tbeg + other.dur and self.tbeg + self.dur > other.tbeg


@dataclass()
class DetectedKWList():
    """
    Metadata of a <detected_kwlist> element in the XML file output by the Index search
    """
    kwid: str
    oov_count: int
    search_time: float
    list_kw: List[DetectedKW]
    
    def merge(self, other: 'DetectedKWList') -> None:
        """
        Merge two DetectedKWList objects, i.e. merge the list of DetectedKW objects
        
        Notes:
        - KWS system outputs are combined by merging their query hits if they refer to the same document and if the time overlaps.
        - Scores are combined by summing them.
        """
        assert self.kwid == other.kwid, f"Cannot merge two DetectedKWList objects with different kwid: {self.kwid} and {other.kwid}"
        for kw in other.list_kw:
            found = False
            for kw2 in self.list_kw:
                if kw.overlap(kw2):
                    kw2.score += kw.score
                    found = True
                    break
            if not found:
                self.list_kw.append(kw)
        return
