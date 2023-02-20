import pytest
from kws.index import Index

DEFAULT_TEST_CTM_FILEPATH = "lib/ctms/reference.ctm"


@pytest.fixture
def index():
    index = Index(ctm_filepath=DEFAULT_TEST_CTM_FILEPATH)
    return index


def test_index_is_non_empty(index):
    assert index.index, "Index is empty"
