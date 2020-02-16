

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    i0 = 40.0
    nMin = -0.1
    nMax = 0.7

    iPulseStrength = 0.0
    resultsFilenamePattern = 'results/integrationINapIKFig4-yyPulseStrength%d.npz'
    phaseFigFilename = 'figures/fig4-yyPhaseSpace.eps'
    voltageFigFilename = 'figures/fig4-yyVoltage.eps'

    plt.figure()
    plotLowThresholdINapIKVectorField(I=i0, nMin=nMin, nMax=nMax)
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

