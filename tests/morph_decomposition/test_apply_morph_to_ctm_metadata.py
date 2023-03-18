from kws.kws_metadata import CTM_metadata
from kws.morph_decomposition.ctm_to_morph import read_morph_dict, apply_morph_to_ctm_metadata




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
