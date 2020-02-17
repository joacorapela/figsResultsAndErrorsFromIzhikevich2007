

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    if len(argv)!=3:
        print("Usage %s <I> <label>"%argv[0])
        return

    i0 = float(argv[1])
    label = argv[2]
    nMin = -0.1
    nMax = 0.7

    resultsFilename= 'results/integrationINapIKFig4-34%s.npz'%label
    phaseFigFilename = 'figures/fig4-34%sPhaseSpace.eps'%label
    voltageFigFilename = 'figures/fig4-34%sVoltage.eps'%label

    plt.figure()
    plotLowThresholdINapIKVectorField(I=i0, nMin=nMin, nMax=nMax)
    results = np.load(resultsFilename)
    ys = results["ys"]
    plt.plot(ys[0, :], ys[1, :], label="I=%d"%i0)
    plt.grid()
    plt.legend()
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')
    plt.savefig(phaseFigFilename)

    times = results["times"]
    plt.figure()
    plt.plot(times, ys[0, :], label="I=%d"%i0)
    results.close()
    plt.grid()
    plt.legend()
    plt.xlabel('Time (secs)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

