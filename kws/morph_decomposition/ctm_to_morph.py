from pathlib import Path
from typing import Dict, List

from kws.index import decode_ctm_line
from kws.kws_metadata import CTM_metadata
from kws.morph_decomposition.utils import load_morph_dict


def apply_morph_to_ctm_metadata(ctm_metadata: CTM_metadata,
                                word_to_morphs: Dict[str, List[str]]) -> List[CTM_metadata]:
    # ------------ EDGE CASE ------------
    if ctm_metadata.word not in word_to_morphs:
        return [ctm_metadata]
    
    
    # ------------ MAIN ------------
    morphs = word_to_morphs[ctm_metadata.word]
    list_new_ctm_metadata = []

    # Common metadata for all morphs:
    morph_dur = ctm_metadata.dur / len(morphs)
    morph_score = ctm_metadata.score ** (1 / len(morphs))
    
    # Iterate over morphs:
    for idx, morph in enumerate(morphs):
        list_new_ctm_metadata.append(CTM_metadata(file=ctm_metadata.file,
                                                  channel=ctm_metadata.channel,
                                                  tbeg=ctm_metadata.tbeg+(idx*morph_dur),
                                                  dur=morph_dur,
                                                  word=morph,
                                                  score=morph_score)
                                    )
    
    return list_new_ctm_metadata


def apply_morph_to_ctm_file(ctm_filepath: str,
                            morph_filepath: str,
                            output_filepath: str) -> None:
    assert Path(ctm_filepath).is_file(), f"CTM file not found: {ctm_filepath}"
    
    word_to_morphs = load_morph_dict(morph_filepath)
    
    list_new_ctm_metadata: List[CTM_metadata] = []
    
    with open(ctm_filepath, "r") as f:
        for ctm_line in f.readlines():
            ctm_metadata = decode_ctm_line(ctm_line)
            list_new_ctm_metadata.extend(
                apply_morph_to_ctm_metadata(ctm_metadata, word_to_morphs=word_to_morphs))
    
    # Format new CTM file:
    new_ctm = ""
    for ctm_metadata in list_new_ctm_metadata:
        new_line = f"{ctm_metadata.file} {ctm_metadata.channel} {ctm_metadata.tbeg:.2f} {ctm_metadata.dur:.2f} {ctm_metadata.word} {ctm_metadata.score:.6f}\n"
        new_ctm += new_line

    # Save new CTM file:
    Path(output_filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(output_filepath, "w") as f:
        f.write(new_ctm)
    
    print(f"New CTM file saved to: {output_filepath}")
    return
