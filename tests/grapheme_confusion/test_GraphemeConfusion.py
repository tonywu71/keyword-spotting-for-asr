from pathlib import Path
import tempfile
from textwrap import dedent
import numpy as np

from kws.grapheme_confusion.grapheme_confusion import GraphemeConfusion


DUMMY_GRAPHEME_MAP_STR = dedent("""\
        j j 14723
        j k 115
        j t 126
        j h 166
        j u 17"""
    )

DUMMY_CTM_STR = dedent("""\
    filename 1 0.0 5.0 k 1.0000
    filename 1 0.0 5.0 t 1.0000
    filename 1 0.0 5.0 h 1.0000
    filename 1 0.0 5.0 u 1.0000""")


def test_similarity_score():
    expected = {
        "j": {
            "k": 0.00759226249422329,
            "t": 0.008318478906714222,
            "h": 0.010959265861226641,
            "u": 0.001122334455667784
        }
    }
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_grapheme_confusion_filepath = Path(temp_dir) / "grapheme.map"
        with open(temp_grapheme_confusion_filepath, "w") as f:
            f.write(DUMMY_GRAPHEME_MAP_STR)
        temp_ctm_filepath = Path(temp_dir) / "dummy.ctm"
        with open(temp_ctm_filepath, "w") as f:
            f.write(DUMMY_CTM_STR)
        
        
        grapheme_confusion = GraphemeConfusion(
                grapheme_confusion_filepath=str(temp_grapheme_confusion_filepath),
                ctm_filepath=str(temp_ctm_filepath)
        )
    
    assert np.isclose(grapheme_confusion._similarity_score("j", "k"), expected["j"]["k"])
    assert np.isclose(grapheme_confusion._similarity_score("j", "t"), expected["j"]["t"])
    assert np.isclose(grapheme_confusion._similarity_score("j", "h"), expected["j"]["h"])
    assert np.isclose(grapheme_confusion._similarity_score("j", "u"), expected["j"]["u"])


def test_closest_iv_word():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_grapheme_confusion_filepath = Path(temp_dir) / "grapheme.map"
        with open(temp_grapheme_confusion_filepath, "w") as f:
            f.write(DUMMY_GRAPHEME_MAP_STR)
        temp_ctm_filepath = Path(temp_dir) / "dummy.ctm"
        with open(temp_ctm_filepath, "w") as f:
            f.write(DUMMY_CTM_STR)
        
        
        grapheme_confusion = GraphemeConfusion(
                grapheme_confusion_filepath=str(temp_grapheme_confusion_filepath),
                ctm_filepath=str(temp_ctm_filepath)
        )
    
    assert grapheme_confusion.get_closest_iv_word(oov_word="j") == "h"
    assert grapheme_confusion.get_closest_iv_word(oov_word="j", subset=set(["k", "t", "u"])) == "t"
