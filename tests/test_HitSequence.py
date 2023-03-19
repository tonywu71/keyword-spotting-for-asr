from kws.hit import Hit, HitSequence

DUMMY_HIT_1 = Hit(file="file1", channel=1, tbeg=0.0, dur=1.0, word="w1", score=1.0)
DUMMY_HIT_2 = Hit(file="file1", channel=1, tbeg=0.5, dur=2.0, word="w2", score=2.0)

DUMMY_HITSEQ = HitSequence(hits=[DUMMY_HIT_1, DUMMY_HIT_2])


def test_hitseq_normalize_scores():
    hitseq = DUMMY_HITSEQ.copy()
    hitseq.normalize_scores(gamma=2.0)
    
    expected_scores = [1/5, 4/5]
    
    assert hitseq[0].score == expected_scores[0], "Hit 1 score is incorrect"
    assert hitseq[1].score == expected_scores[1], "Hit 2 score is incorrect"
    assert hitseq.score == 1.0, "Hit sequence score should be 1.0"
