

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotHighThresholdINapIKVectorField

def main(argv):
    if len(argv)!=3:
        sys.exit("Usage: %s tauV i0"%argv[0])
    aTauV = float(argv[1])
    i0 = float(argv[2])
    tauV = lambda v: aTauV
    resultsFilename = 'results/integrationINapIKFig6-07TauV%.02fI%.02f.npz'%(aTauV, i0)
    phaseFigFilename = 'figures/fig6-07PhaseSpaceTauV%.02fI%.02f.eps'%(aTauV, i0)
    voltageFigFilename = 'figures/fig6-07VoltageTauV%.02fI%.02f.eps'%(aTauV, i0)

    results = np.load(resultsFilename)

    plt.figure()
    plotHighThresholdINapIKVectorField(i=results['i0'])

    plt.plot(results['ys'][0, :], results['ys'][1, :], label="trayectory")
    axes = plt.gca()
    ylim = axes.get_ylim()
    axes.set_ylim((-0.1, ylim[1]))
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig(phaseFigFilename)

    plt.figure()
    plt.plot(results['times'], results['ys'][0, :])
    results.close()
    plt.grid()
    plt.ylim((-90, -30))
    plt.xlim((0, 100))
    plt.axhline(y=-60.9325-11.0, color="black")
    plt.axhline(y=-60.9325+11.0, color="black")
    plt.xlabel('Time (msec)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

