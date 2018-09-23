

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINatVectorField

def main(argv):
    i0 = 0.0
    lowV0 = -60.0
    highV0 = -55.0

    lowV0ResultsFilename='results/integrationINatFig5-6bTopV0%.02f.npz'%lowV0
    highV0ResultsFilename='results/integrationINatFig5-6bTopV0%.02f.npz'%highV0
    phaseFigFilename = 'figures/fig5-6bTopPhaseSpace.eps'
    voltageFigFilename = 'figures/fig5-6bTopVoltage.eps'

    plt.figure()
    plotLowThresholdINatVectorField(i=i0)
    lowV0Results = np.load(lowV0ResultsFilename)
    lowV0Ys = lowV0Results["ys"]
    plt.plot(lowV0Ys[0, :], lowV0Ys[1, :], label="I=%.02f,V0=%.02f"%(i0,lowV0))
    highV0Results = np.load(highV0ResultsFilename)
    highV0Ys = highV0Results["ys"]
    plt.plot(highV0Ys[0, :], highV0Ys[1, :], label="I=%.02f,V0=%.02f"%(i0,highV0))
    # plt.gca().invert_yaxis()
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('Na inactivation, h')
    plt.savefig(phaseFigFilename)

    times = lowV0Results["times"]
    plt.figure()
    plt.plot(times, lowV0Ys[0, :], label="I=%.02f,V0=%.02f"%(i0,lowV0))
    lowV0Results.close()
    plt.plot(times, highV0Ys[0, :], label="I=%.02f,V0=%.02f"%(i0,highV0))
    highV0Results.close()
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

