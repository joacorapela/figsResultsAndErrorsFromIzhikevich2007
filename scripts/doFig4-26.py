

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotHighThresholdINapIKVectorField

def main(argv):
    i0 = 3.0

    iPulseStrength = 1000000
    resultsFilenamePattern = 'results/integrationINapIKFig4-26PulseStrength%d.npz'
    phaseFigFilename = 'figures/fig4-26PhaseSpace.eps'
    voltageFigFilename = 'figures/fig4-26Voltage.eps'

    plt.figure()
    plotHighThresholdINapIKVectorField(i=i0)
    resultsFilename = resultsFilenamePattern % iPulseStrength
    results = np.load(resultsFilename)
    ys = results["ys"]
    plt.plot(ys[0, :], ys[1, :], label="p=%d"%iPulseStrength)
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig(phaseFigFilename)

    times = results["times"]
    plt.figure()
    plt.plot(times, ys[0, :], label="p=%d"%iPulseStrength)
    results.close()
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

