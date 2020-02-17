

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from plotFunctions import plotHighThresholdINapIKVectorField
from utils import getPeakIndices

def main(argv):
    resultsFilename = 'results/integrationINapIKFig10_1.npz'
    aFigFilename = 'figures/fig10_1a.eps'

    results = np.load(resultsFilename)
    times = results['times']
    ys = results['ys']
    spikeIndices = getPeakIndices(v=ys[0,:])
    spikeTimes = times[spikeIndices]

    print("Spike times:")
    print(spikeTimes)

    times = np.delete(times, np.arange(0,spikeIndices[0]))
    spikeTimes = spikeTimes-times[0]
    times = times-times[0]
    ys = np.delete(ys, np.arange(0,spikeIndices[0]), axis=1)
    plt.plot(times, ys[0,:])
    for spikeTime in spikeTimes:
        plt.axvline(x=spikeTime, color="r")
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Potential (mV)")
    plt.savefig(aFigFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

