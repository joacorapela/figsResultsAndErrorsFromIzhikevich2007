

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINatVectorField

def main(argv):
    i0 = 4.0

    resultsFilename='results/integrationINatFig5-6bBottom.npz'
    phaseFigFilename = 'figures/fig5-6bBottomPhaseSpace.eps'
    voltageFigFilename = 'figures/fig5-6bBottomVoltage.eps'

    plt.figure()
    plotLowThresholdINatVectorField(i=i0)
    results = np.load(resultsFilename)
    ys = results["ys"]
    plt.plot(ys[0, :], ys[1, :], label="I=%.02f"%(i0))
    # plt.gca().invert_yaxis()
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('Na inactivation, h')
    plt.savefig(phaseFigFilename)

    times = results["times"]
    plt.figure()
    plt.plot(times, ys[0, :], label="I=%.02f"%(i0))
    results.close()
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

