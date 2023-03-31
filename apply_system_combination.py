from pathlib import Path
import typer
from typing import List, Optional
from kws.system_combination.combine_systems import combine_systems


DEFAULT_SAVEDIR = Path("output/")
DEFAULT_SAVEDIR.mkdir(exist_ok=True)
DEFAULT_OUTPUT_FILENAME = "system_combination.xml"


def main(list_xml_filepath: List[str]) -> None:
    """
    Combine the outputs of multiple KWS systems into a single output.
    
    Notes:
    - KWS system outputs are combined by merging their query hits if they refer to the same document and if the time overlaps.
    - Scores are combined by summing them.
    """
    
    combined_kwlists = combine_systems(list_xml_filepath)
    
    output_filepath = DEFAULT_SAVEDIR / DEFAULT_OUTPUT_FILENAME
    
    with open(output_filepath, 'w') as f:
        f.write('<kwlist kwlist_filename="system_combination" language="swahili" system_id="">\n')
        for kwid, detected_kwlist in combined_kwlists.items():
            f.write(f'  <kw kwid="{kwid}" oov_count="{detected_kwlist.oov_count}" search_time="{detected_kwlist.search_time}">\n')
            for kw in detected_kwlist.list_kw:
                f.write(f'    <kw file="{kw.file}" channel="{kw.channel}" tbeg="{kw.tbeg}" dur="{kw.dur}" word="{kw.word}" score="{kw.score}" decision="{kw.decision}"/>\n')
            f.write('  </kw>\n')
        f.write('</kwlist>')


if __name__ == "__main__":
    typer.run(main)
