from typing import Dict, List
import typer

from pathlib import Path
from tqdm import tqdm
from kws.hit import HitSequence

from kws.index import Index
from kws.query import Queries
from kws.utils import format_all_queries


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main(queries_filepath: str,
         ctm_filepath: str,
         output_filename: str,
         normalize_scores: bool=False,
         gamma: float=1.0):
    """
    Search for queries in CTM file and write output to file.
    """
    queries = Queries.from_file(queries_filepath)
    index = Index(ctm_filepath)
    
    kws_to_hitseqs: Dict[str, List[HitSequence]] = {}
    
    # Perform search for each query:
    tbar = tqdm(queries.queries.items())
    for kwid, query in tbar:
        tbar.set_description(f"Searching for {kwid}")
        list_hitseqs = index.search(query,
                                    normalize_scores=normalize_scores,
                                    gamma=gamma)
        kws_to_hitseqs[kwid] = list_hitseqs
    
    output = format_all_queries(kws_to_hitseqs)
    
    output_filepath = OUTPUT_DIR / output_filename
    with output_filepath.open("w") as output_file:
        output_file.write(output)
    
    print(f"Output succesfully written to {output_filepath}")
    
    return


if __name__ == "__main__":
    typer.run(main)
