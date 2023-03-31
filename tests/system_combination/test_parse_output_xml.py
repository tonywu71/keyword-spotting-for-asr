from pathlib import Path
import tempfile
from textwrap import dedent

from kws.system_combination.utils import parse_output_xml


DUMMY_OUTPUT = dedent("""\
    <kwslist kwlist_filename="dummy.xml" language="swahili" system_id="">

    <detected_kwlist kwid="1" oov_count="0" search_time="0.0">
        <kw file="1.wav" channel="1" tbeg="0.0" dur="0.0" score="0.0" decision="YES"/>
        <kw file="1.wav" channel="1" tbeg="0.0" dur="0.0" score="0.0" decision="YES"/>
    </detected_kwlist>
    <detected_kwlist kwid="2" oov_count="0" search_time="0.0">
        <kw file="2.wav" channel="1" tbeg="0.0" dur="0.0" score="0.0" decision="YES"/>
        <kw file="2.wav" channel="1" tbeg="0.0" dur="0.0" score="0.0" decision="YES"/>
    </detected_kwlist>
    
    </kwslist>
    """)



def test_parse_output_xml():        
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_output_filepath = Path(temp_dir) / "output.xml"
        with open(temp_output_filepath, "w") as f:
            f.write(DUMMY_OUTPUT)
        
        detected_kwlists_dict = parse_output_xml(str(temp_output_filepath))
    
    
    assert len(detected_kwlists_dict) == 2
    
    detected_kwlist = detected_kwlists_dict['1']
    assert detected_kwlist.kwid == '1'
    assert detected_kwlist.oov_count == 0
    assert len(detected_kwlist.list_kw) == 2
    assert detected_kwlist.list_kw[0].file == '1.wav'
    assert detected_kwlist.list_kw[0].channel == 1
    assert detected_kwlist.list_kw[0].tbeg == 0.0
    assert detected_kwlist.list_kw[0].dur == 0.0
    assert detected_kwlist.list_kw[0].score == 0.0
    assert detected_kwlist.list_kw[0].decision == True
    assert detected_kwlist.list_kw[1].file == '1.wav'
    assert detected_kwlist.list_kw[1].channel == 1
    assert detected_kwlist.list_kw[1].tbeg == 0.0
    assert detected_kwlist.list_kw[1].dur == 0.0
    assert detected_kwlist.list_kw[1].score == 0.0
    assert detected_kwlist.list_kw[1].decision == True
    
    detected_kwlist = detected_kwlists_dict['2']
    assert detected_kwlist.kwid == '2'
    assert detected_kwlist.oov_count == 0
    assert len(detected_kwlist.list_kw) == 2
    assert detected_kwlist.list_kw[0].file == '2.wav'
    assert detected_kwlist.list_kw[0].channel == 1
    assert detected_kwlist.list_kw[0].tbeg == 0.0
    assert detected_kwlist.list_kw[0].dur == 0.0
    assert detected_kwlist.list_kw[0].score == 0.0
    assert detected_kwlist.list_kw[0].decision == True
