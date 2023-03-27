score-reference:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference.xml


score-reference-normalized:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference-normalized.xml --normalize-scores


score-reference-morph:
	python search.py lib/kws/queries-morph.xml lib/ctms/reference-morph.ctm reference-morph.xml


score-reference-grapheme_confusion:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference-grapheme_confusion.xml --use-grapheme-confusion


score-reference-normalized-grapheme_confusion:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference-normalized_with_grapheme_confusion.xml --normalize-scores --use-grapheme-confusion


score-decode:
	python search.py lib/kws/queries.xml lib/ctms/decode.ctm decode.xml


score-decode-morph:
	python search.py lib/kws/queries-morph.xml lib/ctms/decode-morph.ctm decode-morph.xml


eval-reference:
	rm -rf scoring/* \
	&& scripts/score.sh output/reference.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring oov


eval-reference-grapheme_confusion:
	rm -rf scoring/* \
	&& scripts/score.sh output/reference-grapheme_confusion.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-grapheme_confusion.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-grapheme_confusion.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-grapheme_confusion.xml scoring oov


eval-decode:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode.xml scoring oov


eval-decode-grapheme_confusion:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-grapheme_confusion.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-grapheme_confusion.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-grapheme_confusion.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-grapheme_confusion.xml scoring oov


apply_morph_to_ctm:
	python apply_morph_to_ctm.py lib/ctms/reference.ctm lib/dicts/morph.dct reference-morph.ctm


apply_morph_to_ctm:
	python apply_morph_to_queries.py lib/kws/queries.xml lib/dicts/morph.dct queries-morph.xml
