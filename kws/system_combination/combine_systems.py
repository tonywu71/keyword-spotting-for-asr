from typing import Dict, List
from kws.system_combination.detected_kwlist import DetectedKWList
from kws.system_combination.utils import parse_output_xml


def combine_systems(list_xml_filepath: List[str]) -> Dict[str, DetectedKWList]:
    """
    Combine the outputs of multiple KWS systems into a single output.
    
    Notes:
    - KWS system outputs are combined by merging their query hits if they refer to the same document and if the time overlaps.
    - Scores are combined by summing them.
    """
    
    # Parse the output of each system
    list_kwid_to_detected_kwlist = [parse_output_xml(filepath) for filepath in list_xml_filepath]
    
    answer: Dict[str, DetectedKWList] = {}
    
    for kwid_to_detected_kwlist in list_kwid_to_detected_kwlist:
        for kwid, detected_kwlist in kwid_to_detected_kwlist.items():
            if kwid not in answer:
                answer[kwid] = detected_kwlist
            else:
                answer[kwid].merge(detected_kwlist)
    
    return answer
