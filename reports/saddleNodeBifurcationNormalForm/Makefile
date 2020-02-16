
all: snBifNormalForm.ps

snBifNormalForm.dvi: snBifNormalForm.tex
	latex snBifNormalForm
	bibtex snBifNormalForm
	latex snBifNormalForm
	latex snBifNormalForm

snBifNormalForm.ps: snBifNormalForm.dvi
	dvips snBifNormalForm
