from kws.hit import Hit, HitSequence, normalize_scores_hitseqs


def test_hitseq_normalize_scores():
    dummy_hitseq_1 = HitSequence(hits=[Hit(file="file1", channel=1, tbeg=0.0, dur=1.0, word="w1", score=1.0)])
    dummy_hitseq_2 = HitSequence(hits=[Hit(file="file1", channel=1, tbeg=0.5, dur=2.0, word="w1", score=2.0)])
    list_hitseqs = [dummy_hitseq_1, dummy_hitseq_2]
    
    normalize_scores_hitseqs(list_hitseqs=list_hitseqs, gamma=2.0)
    
    expected_scores = [1/5, 4/5]
    
    assert list_hitseqs[0].score == expected_scores[0], "Hit 1 score is incorrect"
    assert list_hitseqs[1].score == expected_scores[1], "Hit 2 score is incorrect"
