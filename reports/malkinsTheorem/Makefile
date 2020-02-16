
all: malkinsTheorem.pdf

%.pdf: %.tex
	latex $*
	bibtex $*
	latex $*
	latex $*
	dvipdf $*

clean:
	rm *.aux \
       *.out \
	   *.bbl \
	   *.pdf \
	   *.blg \
       *.log

touch:
	touch *.tex
