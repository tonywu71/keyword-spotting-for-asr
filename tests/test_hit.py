from kws.hit import Hit

DUMMY_HIT_1 = Hit(file="file1", channel=1, tbeg=0.0, dur=1.0, score=0.5)
DUMMY_HIT_2 = Hit(file="file1", channel=1, tbeg=0.5, dur=2.0, score=0.5)


def test_hit_detect_overlap():
    assert DUMMY_HIT_1.overlaps_with(DUMMY_HIT_2), "Hits should overlap"
