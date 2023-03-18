from pathlib import Path
import tempfile
from kws.kws_metadata import CTM_metadata
from kws.morph_decomposition.ctm_to_morph import get_word_to_morphs_dict, apply_morph_to_ctm_metadata

def test_get_word_to_morphs_dict():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "morphs.txt"
        with open(temp_file, "w") as f:
            f.write("a   a_1\n")
            f.write("b   b_1 b_2\n")
            f.write("c   c_1 c_2 c_3\n")
        
        word_to_morphs = get_word_to_morphs_dict(str(temp_file))
        
        assert word_to_morphs["a"] == ["a_1"]
        assert word_to_morphs["b"] == ["b_1", "b_2"]
        assert word_to_morphs["c"] == ["c_1", "c_2", "c_3"]


def test_apply_morph_to_ctm_metadata():
    ctm_metadata = CTM_metadata(file="file",
                                channel=1,
                                tbeg=0.0,
                                dur=1.0,
                                word="a",
                                score=0.04)
    
    word_to_morphs = {"a": ["a_1", "a_2"]}
    
    list_new_ctm_metadata = apply_morph_to_ctm_metadata(ctm_metadata, word_to_morphs=word_to_morphs)
    
    expected_ctm_metadata = [
        CTM_metadata(file="file",
                     channel=1,
                     tbeg=0.0,
                     dur=0.5,
                     word="a_1",
                     score=0.2),
        CTM_metadata(file="file",
                     channel=1,
                     tbeg=0.0,
                     dur=0.5,
                     word="a_2",
                     score=0.2)
    ]
    
    for ctm_metadata, expected_ctm_metadata in zip(list_new_ctm_metadata, expected_ctm_metadata):
        assert ctm_metadata == expected_ctm_metadata
