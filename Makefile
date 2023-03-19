score-reference:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference.xml


score-reference-normalized:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference.xml --normalize_scores


score-reference-grapheme_confusion:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference.xml --use_grapheme_confusion


score-reference-normalized-grapheme_confusion:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference.xml --normalize_scores --use_grapheme_confusion


eval-reference:
	rm -rf scoring/reference \
	scripts/score.sh output/reference.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring oov


apply_morph_to_ctm:
	python apply_morph_to_ctm.py lib/ctms/reference.ctm lib/dicts/morph.dct reference-morph.ctm


apply_morph_to_ctm:
	python apply_morph_to_queries.py lib/kws/queries.xml lib/dicts/morph.dct queries-morph.xml
