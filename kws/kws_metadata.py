from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CTM_metadata():
    """
    Metadata of a word in a Conversation Time Marked (CTM) file
    Attributes:
    - file = name of the audio file
    - channel = channel of the audio file
    - tbeg = start time of the word in seconds
    - dur = duration of the word in seconds
    - word
    - score = score of the word
    - next_word = word that follows the current word in the same utterance
    
    Note the next_word is not part of the CTM format, but storing it here
    greatly speeds up the search for hits in index search.
    """
    file: str
    channel: int
    tbeg: float
    dur: float
    word: str
    score: float
    next_word: Optional[str]=None
