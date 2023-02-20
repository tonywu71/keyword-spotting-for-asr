from __future__ import annotations
from kws.index import CTM_metadata


class Hit:
    def __init__(self, file: str, channel: int, tbeg: float, dur: float, score: float):
        self.file = file
        self.channel = channel
        self.tbeg = tbeg
        self.dur = dur
        self.score = score

    
    @classmethod
    def from_ctm_metadata(cls, ctm_metadata: CTM_metadata):
        """Create a Hit from a CTM_metadata object"""
        return cls(file=ctm_metadata.file,
                   channel=ctm_metadata.channel,
                   tbeg=ctm_metadata.tbeg,
                   dur=ctm_metadata.dur,
                   score=ctm_metadata.score)

    
    def __str__(self):
        return (f"Hit(file={self.file}, channel={self.channel}, "
                f"tbeg={self.tbeg}, dur={self.dur}, score={self.score})")
    
    
    def overlaps_with(self, hit_2: Hit) -> bool:
        start1, start2 = self.tbeg, hit_2.tbeg
        end1, end2 = start1 + self.dur, start2 + hit_2.dur
        return (start1 <= end2) and (start2 <= end1)
