score-reference:
	python search.py lib/kws/queries.xml lib/ctms/reference.ctm reference.xml

eval-reference:
	rm -rf scoring/reference \
	scripts/score.sh output/reference.xml scoring \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring all \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring iv \
	&& scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring oov
