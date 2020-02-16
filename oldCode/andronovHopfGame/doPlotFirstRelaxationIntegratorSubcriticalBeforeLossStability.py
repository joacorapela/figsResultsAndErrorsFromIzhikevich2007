
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from FirstRelaxationOscillator import FirstRelaxationOscillator

def main(argv):
    resultsUnstableLCFilename = 'results/integrationFirstRelaxationOscillatorSubcriticalBeforeLossOfStabilityUnstableLC.npz'
    resultsInsideFilename = 'results/integrationFirstRelaxationOscillatorSubcriticalBeforeLossOfStabilityStartInsideUnstableLC.npz'
    resultsOutsideFilename = 'results/integrationFirstRelaxationOscillatorSubcriticalBeforeLossOfStabilityStartOutsideUnstableLC.npz'
    figFilename = 'figures/phaseSpaceFirstRelaxationOscillatorSubcriticalBeforeLossOfStability.eps'
    f = lambda x: np.exp(x)*x**2
    b = -0.1

    vEq = b
    uEq = f(b)

    ysUnstableLC = np.load(resultsUnstableLCFilename)['ys']
    ysInside = np.load(resultsInsideFilename)['ys']
    v0Inside = ysInside[0,0]
    u0Inside = ysInside[1,0]
    ysOutside = np.load(resultsOutsideFilename)['ys']
    v0Outside = ysOutside[0,0]
    u0Outside = ysOutside[1,0]

    eqMarker = 'o'
    eqCol = 'grey'
    eqSize = 8
    startMarker = 'x'
    startCol = 'red'
    startSize = 8
    traceMarker = '.'
    unstableLCTraceCol = 'grey'
    insideTraceCol = 'blue'
    outsideTraceCol = 'red'
    traceSize = 1
    xlim = (-1, 1)
    ylim = (-1, 1)

    plt.plot(vEq, uEq, color=eqCol, marker=eqMarker,
                  markerfacecolor=eqCol, markersize=eqSize)
    plt.plot(ysUnstableLC[0, :], ysUnstableLC[1, :], color=unstableLCTraceCol, marker=traceMarker, markersize=traceSize)
    plt.plot(v0Inside, u0Inside, color=startCol, marker=startMarker, markersize=startSize)
    plt.plot(ysInside[0, :], ysInside[1, :], color=insideTraceCol, marker=traceMarker, markersize=traceSize)
    plt.plot(v0Outside, u0Outside, color=startCol, marker=startMarker, markersize=startSize)
    plt.plot(ysOutside[0, :], ysOutside[1, :], color=outsideTraceCol, marker=traceMarker, markersize=traceSize)
    plt.grid()
    plt.xlabel('v')
    plt.ylabel('u')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

