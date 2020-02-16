
all: andronovHopfBifurcations

andronovHopfBifurcations: andronovHopfBifurcations.tex \
../../andronovHopfGame/figures/phaseSpaceFirstRelaxationOscillatorSupercriticalBeforeLossOfStability.eps \
../../andronovHopfGame/figures/phaseSpaceFirstRelaxationOscillatorSupercriticalAfterLossOfStability.eps \
../../andronovHopfGame/figures/phaseSpaceFirstRelaxationOscillatorSubcriticalBeforeLossOfStability.eps \
../../andronovHopfGame/figures/phaseSpaceFirstRelaxationOscillatorSubcriticalAfterLossOfStability.eps 
	latex andronovHopfBifurcations
	latex andronovHopfBifurcations
	bibtex andronovHopfBifurcations
	latex andronovHopfBifurcations
	dvips andronovHopfBifurcations
