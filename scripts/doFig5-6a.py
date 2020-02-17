

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotHighThresholdINatVectorField

def main(argv):
    if len(argv)!=3:
        print("Usage %s <I> <label>"%argv[0])
        return

    i0 = float(argv[1])
    label = argv[2]

    resultsFilename= 'results/integrationINatFig5-6a%s.npz'%label
    phaseFigFilename = 'figures/fig5-6a%sPhaseSpace.eps'%label
    voltageFigFilename = 'figures/fig5-6a%sVoltage.eps'%label

    plt.figure()
    plotHighThresholdINatVectorField(i=i0)
    results = np.load(resultsFilename)
    ys = results["ys"]
    plt.plot(ys[0, :], ys[1, :], label="I=%.02f"%i0)
    # plt.gca().invert_yaxis()
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('Na inactivation, h')
    plt.savefig(phaseFigFilename)

    times = results["times"]
    plt.figure()
    plt.plot(times, ys[0, :], label="I=%.02f"%i0)
    results.close()
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

