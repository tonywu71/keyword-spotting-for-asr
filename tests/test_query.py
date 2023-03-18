import pytest
from kws.query import Queries

DEFAULT_TEST_QUERIES_FILEPATH = "lib/kws/queries.xml"


@pytest.fixture
def queries() -> Queries:
    queries = Queries.from_file(queries_filepath=DEFAULT_TEST_QUERIES_FILEPATH)
    return queries


def test_queries_is_non_empty(queries: Queries):
    assert queries.queries, "Queries is empty"


def test_queries_to_xml(queries: Queries):
    xml = queries.to_xml()
    new_queries = Queries.from_str(xml)
    new_xml = new_queries.to_xml()
    
    assert xml == new_xml, "XML is not the same after parsing and unparsing"
