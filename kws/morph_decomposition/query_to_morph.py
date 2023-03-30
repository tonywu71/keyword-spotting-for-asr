from typing import Dict, List
from pathlib import Path

from kws.morph_decomposition.utils import load_morph_dict
from kws.query import Query, Queries


def apply_morph_to_query(query: Query,
                         word_to_morphs: Dict[str, List[str]]) -> Query:
    list_queries: List[Query] = []
    
    for word in query.kwtext:
        if word not in word_to_morphs:
            list_queries.append(Query(kwid=query.kwid, kwtext=word))
        else:
            for morph in word_to_morphs[word]:
                list_queries.append(Query(kwid=query.kwid, kwtext=morph))
    
    new_query = Query(kwid=query.kwid, kwtext=" ".join([" ".join(q.kwtext) for q in list_queries]))
    return new_query


def apply_morph_to_queries_file(queries_filepath: str,
                                morph_filepath: str,
                                output_filepath: str) -> None:
    assert Path(queries_filepath).is_file(), f"Query file not found: {queries_filepath}"
    queries = Queries.from_file(queries_filepath)
    
    word_to_morphs = load_morph_dict(morph_filepath)
    
    list_new_queries: List[Query] = []
    
    for kwid, list_queries in queries.kwid_to_list_queries.items():
        for query in list_queries:
            list_new_queries.append(apply_morph_to_query(query, word_to_morphs=word_to_morphs))
    
    # Create new Queries object:
    new_queries = Queries.from_list_of_queries(list_new_queries)

    # Save new Queries file:
    Path(output_filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(output_filepath, "w") as f:
        f.write(new_queries.to_xml())
    
    print(f"New Queries file saved to: {output_filepath}")
    return
