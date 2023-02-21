import pytest
from kws.query import Query
from kws.index import Index

DEFAULT_TEST_CTM_FILEPATH = "lib/ctms/reference.ctm"


@pytest.fixture
def index():
    index = Index(ctm_filepath=DEFAULT_TEST_CTM_FILEPATH)
    return index


@pytest.fixture
def query_word():
    query = Query(kwid="1", kwtext="nimwachie")
    return query


@pytest.fixture
def query_phrase():
    query = Query(kwid="1", kwtext="habari ya")
    return query


def test_index_is_non_empty(index):
    assert index.index, "Index is empty"


def test_index_search_word(index, query_word):
    list_hitseqs = index.search(query_word)
    assert list_hitseqs, "Word not found"
    assert len(list_hitseqs) == 1, "HitSequence is not a singleton"


def test_index_search_phrase(index, query_phrase):
    list_hitseqs = index.search(query_phrase)
    assert list_hitseqs, "Phrase not found"
    assert all(len(hitseq) <= len(query_phrase.kwtext) for hitseq in list_hitseqs), \
        f"HitSequence is longer than query: {query_phrase.kwtext}"
