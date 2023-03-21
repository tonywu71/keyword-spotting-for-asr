from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CTM_metadata():
    """
    Metadata of a word in a Conversation Time Marked (CTM) file
    Note:
    - tbeg = start time of the word in seconds
    - dur = duration of the word in seconds
    """
    file: str
    channel: int
    tbeg: float
    dur: float
    word: str
    score: float
    next_word: Optional[str]=None
