from pathlib import Path
import tempfile
from textwrap import dedent

from kws.grapheme_confusion.utils import load_grapheme_confusion


DUMMY_GRAPHEME_MAP_STR = dedent("""\
        j j 14723
        j k 115
        j t 126
        j h 166
        j u 17"""
    )


def test_load_grapheme_confusion():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "grapheme.map"
        with open(temp_file, "w") as f:
            f.write(DUMMY_GRAPHEME_MAP_STR)
        
        grapheme_confusion = load_grapheme_confusion(str(temp_file))
        
        expected_sum = 14723 + 115 + 126 + 166 + 17
        
        assert grapheme_confusion["j"]["j"] == 14723 / expected_sum
        assert grapheme_confusion["j"]["k"] == 115 / expected_sum
        assert grapheme_confusion["j"]["t"] == 126 / expected_sum
        assert grapheme_confusion["j"]["h"] == 166 / expected_sum
        assert grapheme_confusion["j"]["u"] == 17 / expected_sum
