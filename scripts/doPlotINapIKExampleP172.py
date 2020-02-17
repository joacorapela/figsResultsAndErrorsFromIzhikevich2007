

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    if len(argv)!=3:
        sys.exit("Usage: %s i0 a"%argv[0])
    i0 = float(argv[1])
    a = float(argv[2])
    resultsFilename = 'results/integrationINapIKExampleP172I%.02fa%f.npz'%(i0,a)
    phaseFigFilename = 'figures/figPhaseSpaceExampleINapIKP172I%.02fa%f.eps'%(i0,a)
    voltageFigFilename = 'figures/figVoltageExampleINapIKP172I%.02fa%f.eps'%(i0,a)

    results = np.load(resultsFilename)

    plt.figure()
    plotLowThresholdINapIKVectorField(i=results['i0'])

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
    plt.xlabel('Time (msec)')
    plt.ylabel('Voltage (mv)')
    plt.savefig(voltageFigFilename)

    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

