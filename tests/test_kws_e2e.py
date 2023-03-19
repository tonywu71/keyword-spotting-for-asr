import pytest

from tqdm.auto import tqdm
from kws.index import Index
from kws.query import Queries

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
    for kwid, query in tqdm(queries.queries.items()):
        list_hitseqs = index.search(query)
        assert all(histseq.score == 1. for histseq in list_hitseqs), f"Query score is not 1: {query.kwtext}"


def test_e2e_index_search_score_normalization(queries: Queries, index: Index):
    for kwid, query in tqdm(queries.queries.items()):
        list_hitseqs = index.search(query, normalize_scores=True, gamma=DEFAULT_GAMMA)
        for hitseq in list_hitseqs:
            assert hitseq.score == 1.0, f"Hit sequence score is not 1: {query.kwtext}"
