from pathlib import Path
from typing import Dict

from bs4 import BeautifulSoup

from kws.system_combination.detected_kwlist import DetectedKW, DetectedKWList


def parse_output_xml(filepath: str) -> Dict[str, DetectedKWList]:
    assert Path(filepath).exists(), f"File {filepath} does not exist"
    
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f.read(), 'xml')
        
    list_detected_kwlist = soup.find_all('detected_kwlist')
    detected_kwlists_dict = {}
    
    for detected_kwlist in list_detected_kwlist:
        kwid = detected_kwlist['kwid']
        oov_count = int(detected_kwlist['oov_count'])
        search_time = float(detected_kwlist['search_time'])
        list_kw = []
        for kw in detected_kwlist.find_all('kw'):            
            file = kw['file']
            channel = int(kw['channel'])
            tbeg = float(kw['tbeg'])
            dur = float(kw['dur'])
            score = float(kw['score'])
            decision = True if kw['decision'] == 'YES' else False
            detected_kw = DetectedKW(file=file, channel=channel, tbeg=tbeg, dur=dur, score=score, decision=decision)
            list_kw.append(detected_kw)
        detected_kwlist = DetectedKWList(kwid=kwid, oov_count=oov_count, search_time=search_time, list_kw=list_kw)
        detected_kwlists_dict[kwid] = detected_kwlist
        
    return detected_kwlists_dict
