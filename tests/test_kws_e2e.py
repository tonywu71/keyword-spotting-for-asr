from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, List
import pytest

from tqdm.auto import tqdm
from kws.hit import HitSequence
from kws.index import Index
from kws.query import Queries
from kws.utils import format_all_queries

DEFAULT_TEST_QUERIES_FILEPATH = "lib/kws/queries.xml"
DEFAULT_TEST_CTM_FILEPATH = "lib/ctms/reference.ctm"

DEFAULT_GAMMA = 2.0


@pytest.fixture
def queries() -> Queries:
    queries = Queries.from_file(queries_filepath=DEFAULT_TEST_QUERIES_FILEPATH)
    return queries


@pytest.fixture
def index() -> Index:
    index = Index(ctm_filepath=DEFAULT_TEST_CTM_FILEPATH)
    return index


def test_e2e_index_search_from_reference_all_1(queries: Queries, index: Index):
    for kwid, list_queries in tqdm(queries.kwid_to_list_queries.items()):
        for query in list_queries:
            list_hitseqs = index.search(query)
            assert all(hitseq.score == 1. for hitseq in list_hitseqs), f"Query score is not 1: {query.kwtext}"


def test_e2e_index_search_from_reference_match_expected_output(queries: Queries, index: Index):
    EXPECTED_OUTPUT_FILEPATH = Path("tests/expected_reference_output.xml")
    assert EXPECTED_OUTPUT_FILEPATH.is_file(), "Expected output file not found"
    expected_output = EXPECTED_OUTPUT_FILEPATH.read_text()
    
    kws_to_hitseqs: DefaultDict[str, List[HitSequence]] = defaultdict(list)
    
    # Perform search for each query:
    tbar = tqdm(queries.kwid_to_list_queries.items())
    for kwid, list_queries in tbar:
        for query in list_queries:
            tbar.set_description(f"Searching for {kwid}")
            list_hitseqs = index.search(query)
            kws_to_hitseqs[kwid].extend(list_hitseqs)
    
    output = format_all_queries(kws_to_hitseqs)
    
    assert output == expected_output, "Output does not match expected output"
