from kws.grapheme_confusion.grapheme_confusion import GraphemeConfusionBase


def test_levenshtein_distance_with_unit_cost():
    grapheme_confusion = GraphemeConfusionBase()
    assert grapheme_confusion._levenshtein_distance("a", "a") == 0
    assert grapheme_confusion._levenshtein_distance("a", "b") == 1
    assert grapheme_confusion._levenshtein_distance("ab", "ba") == 2
    assert grapheme_confusion._levenshtein_distance("ab", "bc") == 2
    assert grapheme_confusion._levenshtein_distance("ab", "ac") == 1
    assert grapheme_confusion._levenshtein_distance("ab", "ab") == 0
    assert grapheme_confusion._levenshtein_distance("ab", "a") == 1
    assert grapheme_confusion._levenshtein_distance("ab", "b") == 1
    assert grapheme_confusion._levenshtein_distance("ab", "c") == 2
    assert grapheme_confusion._levenshtein_distance("a", "ab") == 1
    assert grapheme_confusion._levenshtein_distance("b", "ab") == 1
    assert grapheme_confusion._levenshtein_distance("c", "ab") == 2
    assert grapheme_confusion._levenshtein_distance("abc", "a") == 2
    assert grapheme_confusion._levenshtein_distance("abc", "b") == 2
    assert grapheme_confusion._levenshtein_distance("abc", "c") == 2
    assert grapheme_confusion._levenshtein_distance("abc", "ab") == 1
    assert grapheme_confusion._levenshtein_distance("abc", "bc") == 1
    assert grapheme_confusion._levenshtein_distance("abc", "ac") == 1
    assert grapheme_confusion._levenshtein_distance("abc", "ac") == 1
    assert grapheme_confusion._levenshtein_distance("abc", "abc") == 0
    assert grapheme_confusion._levenshtein_distance("abc", "bac") == 2
    assert grapheme_confusion._levenshtein_distance("abc", "acb") == 2
    assert grapheme_confusion._levenshtein_distance("abc", "cab") == 2
    assert grapheme_confusion._levenshtein_distance("abc", "cba") == 2
    assert grapheme_confusion._levenshtein_distance("abc", "d") == 3
    assert grapheme_confusion._levenshtein_distance("abc", "e") == 3
