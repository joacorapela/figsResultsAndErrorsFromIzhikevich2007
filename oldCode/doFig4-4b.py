

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    phaseFigFilename = 'figures/fig4-4bPhaseSpace.eps'
    voltageFigFilename = 'figures/fig4-4bVoltage.eps'
    resultsFilenamePattern = 'results/integrationINapIKStepsize%d.npz'
    i0 = 40

    resultsFilename = resultsFilenamePattern % i0
    results = np.load(resultsFilename)
    plt.figure()
    plotLowThresholdINapIKVectorField()

    plt.plot(results['ys'][0, :], results['ys'][1, :], label="%d"%i0)
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig(phaseFigFilename)

    plt.figure()
    plt.plot(results['times'], results['ys'][0, :], label="%d"%i0)
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

