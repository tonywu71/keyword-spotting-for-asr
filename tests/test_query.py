import pytest
from kws.query import Queries

DEFAULT_TEST_QUERIES_FILEPATH = "lib/kws/queries.xml"


@pytest.fixture
def queries():
    queries = Queries(queries_filepath=DEFAULT_TEST_QUERIES_FILEPATH)
    return queries


def test_queries_is_non_empty(queries):
    assert queries.queries, "Queries is empty"
