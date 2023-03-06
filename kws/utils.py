from typing import Dict, List
from kws.hit import HitSequence

HITS_FILE_HEADER = '<kwslist kwlist_filename="IARPA-babel202b-v1.0d_conv-dev.kwlist.xml" language="swahili" system_id="">\n'
HITS_FILE_FOOTER = '</kwslist>'
HIT_HEADER = '<detected_kwlist kwid="{kwid}" oov_count="0" search_time="0.0">\n'
HIT_FOOTER = '</detected_kwlist>\n'
# Note: HIT_HEADER contains a kwid field, which should be filled in using the format method


def format_single_query(kwid: str, histseq: HitSequence):
    output = ""
    
    output += HIT_HEADER.format(kwid=kwid)
    output += str(histseq)
    output += HIT_FOOTER
    
    return output


def format_all_queries(kws_to_hitseqs: Dict[str, List[HitSequence]]) -> str:
    output = ""
    
    output += HITS_FILE_HEADER
    
    for kwid, list_hitseqs in kws_to_hitseqs.items():
        for histseq in list_hitseqs:
            output += format_single_query(kwid, histseq)
            
    output += HITS_FILE_FOOTER
    
    return output
