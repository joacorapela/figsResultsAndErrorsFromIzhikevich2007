
all: andronovHopfBifurcations.pdf

andronovHopfBifurcations.pdf: andronovHopfBifurcations.tex
	latex andronovHopfBifurcations
	bibtex andronovHopfBifurcations
	latex andronovHopfBifurcations
	latex andronovHopfBifurcations
	dvipdf andronovHopfBifurcations

clean:
	rm andronovHopfBifurcations.aux \
       andronovHopfBifurcations.out \
	   andronovHopfBifurcations.bbl \
	   andronovHopfBifurcations.pdf \
	   andronovHopfBifurcations.blg \
       andronovHopfBifurcations.log
