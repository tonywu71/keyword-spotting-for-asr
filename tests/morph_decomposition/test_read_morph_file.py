from pathlib import Path
import tempfile

from kws.morph_decomposition.utils import read_morph_dict


def test_read_morph_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "morphs.txt"
        with open(temp_file, "w") as f:
            f.write("a   a_1\n")
            f.write("b   b_1 b_2\n")
            f.write("c   c_1 c_2 c_3\n")
        
        word_to_morphs = read_morph_dict(str(temp_file))
        
        assert word_to_morphs["a"] == ["a_1"]
        assert word_to_morphs["b"] == ["b_1", "b_2"]
        assert word_to_morphs["c"] == ["c_1", "c_2", "c_3"]
