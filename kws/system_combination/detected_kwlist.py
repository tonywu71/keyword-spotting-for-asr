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
    word: str
    score: float
    decision: bool


@dataclass()
class DetectedKWList():
    """
    Metadata of a <detected_kwlist> element in the XML file output by the Index search
    """
    kwid: str
    oov_count: int
    search_time: float
    list_kw: List[DetectedKW]
