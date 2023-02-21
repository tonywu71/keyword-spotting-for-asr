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
    assert index.search(query_word), "Word not found"


def test_index_search_phrase(index, query_phrase):
    assert len(index.search(query_phrase)) >= 2, "Phrase not found"
