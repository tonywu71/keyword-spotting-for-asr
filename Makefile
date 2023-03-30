# ---- SCORING ----

score-reference:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference.xml


score-reference-normalized:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference-normalized.xml --normalize-scores


score-reference-morph:
	python search.py lib/kws/queries-morph.xml lib/ctms/reference-morph.ctm reference-morph-custom.xml


score-reference-grapheme_confusion:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference-grapheme_confusion.xml --use-grapheme-confusion


score-reference-normalized-grapheme_confusion:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference-normalized-grapheme_confusion.xml --normalize-scores --use-grapheme-confusion


score-decode:
	python search.py lib/kws/queries.xml lib/ctms/decode.ctm decode.xml


score-decode-morph:
	python search.py lib/kws/queries-morph.xml lib/ctms/decode-morph.ctm decode-morph.xml


score-decode-morph-custom:
	python search.py lib/kws/queries-morph.xml lib/ctms/decode-morph-custom.ctm decode-morph-custom.xml


score-decode-normalized:
	python search.py lib/kws/queries.xml lib/ctms/decode.ctm decode-normalized.xml --normalize-scores


score-decode-morph-normalized:
	python search.py lib/kws/queries-morph.xml lib/ctms/decode-morph.ctm decode-morph-normalized.xml --normalize-scores


score-decode-morph-custom-normalized:
	python search.py lib/kws/queries-morph.xml lib/ctms/decode-morph-custom.ctm decode-morph-custom-normalized.xml --normalize-scores


score-decode-grapheme_confusion:
	python search.py lib/kws/queries.xml lib/ctms/decode.ctm decode-grapheme_confusion.xml --use-grapheme-confusion


score-decode-normalized-grapheme_confusion:
	python search.py lib/kws/queries.xml lib/ctms/decode.ctm decode-normalized-grapheme_confusion.xml --normalize-scores --use-grapheme-confusion


score-decode-morph-grapheme_confusion:
	python search.py lib/kws/queries-morph.xml lib/ctms/decode.ctm decode-morph-grapheme_confusion.xml --use-grapheme-confusion


score-decode-morph-normalized-grapheme_confusion:
	python search.py lib/kws/queries-morph.xml lib/ctms/decode.ctm decode-morph-normalized-grapheme_confusion.xml --normalize-scores --use-grapheme-confusion



# ---- EVALUATION ----

eval-reference:
	rm -rf scoring/* \
	&& scripts/score.sh output/reference.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring oov


eval-reference-morph:
	rm -rf scoring/* \
	&& scripts/score.sh output/reference-morph-custom.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-morph-custom.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-morph-custom.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-morph-custom.xml scoring oov


eval-reference-normalized:
	rm -rf scoring/* \
	&& scripts/score.sh output/reference-normalized.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-normalized.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-normalized.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference-normalized.xml scoring oov


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


eval-decode-morph:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-morph.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph.xml scoring oov


eval-decode-morph-custom:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-morph-custom.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-custom.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-custom.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-custom.xml scoring oov


eval-decode-normalized:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-normalized.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-normalized.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-normalized.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-normalized.xml scoring oov


eval-decode-morph-normalized:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-morph-normalized.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-normalized.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-normalized.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-normalized.xml scoring oov


eval-decode-morph-custom-normalized:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-morph-custom-normalized.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-custom-normalized.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-custom-normalized.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-custom-normalized.xml scoring oov


eval-decode-grapheme_confusion:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-grapheme_confusion.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-grapheme_confusion.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-grapheme_confusion.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-grapheme_confusion.xml scoring oov


eval-decode-normalized-grapheme_confusion:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-normalized-grapheme_confusion.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-normalized-grapheme_confusion.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-normalized-grapheme_confusion.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-normalized-grapheme_confusion.xml scoring oov


eval-decode-morph-grapheme_confusion:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-morph-grapheme_confusion.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-grapheme_confusion.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-grapheme_confusion.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-grapheme_confusion.xml scoring oov


eval-decode-morph-normalized-grapheme_confusion:
	rm -rf scoring/* \
	&& scripts/score.sh output/decode-morph-normalized-grapheme_confusion.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-normalized-grapheme_confusion.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-normalized-grapheme_confusion.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/decode-morph-normalized-grapheme_confusion.xml scoring oov



# ---- APPLY MORPH TRANSFORMATION ----

apply_morph_to_ctm:
	python apply_morph_to_ctm.py lib/ctms/reference.ctm lib/dicts/morph.dct reference-morph-custom.ctm \
	&& python apply_morph_to_ctm.py lib/ctms/decode.ctm lib/dicts/morph.dct decode-morph-custom.ctm


apply_morph_to_queries:
	python apply_morph_to_queries.py lib/kws/queries.xml lib/dicts/morph.kwslist.dct queries-morph.xml
