
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from utils import getPeakIndices

def main(argv):
    resultsFilename = 'results/integrationINapIKFig10_10.npz'
    figFilename = 'figures/fig10_10c.eps'
    nPhases = 7
    fontsize = 20
    marker = "o"

    results = np.load(resultsFilename)

    pulseTimes = results["offset"]+\
                  np.arange(start=0, stop=nPhases, step=1)*results["Ts"]

    spikeIndices = getPeakIndices(v=results["ys"][0,:])
    spikeTimes = results["times"][spikeIndices]

    pulsePhases = np.empty(pulseTimes.shape)
    for i in range(len(pulsePhases)):
        precedingSpikeIndex = np.nonzero(spikeTimes<pulseTimes[i])[0][-1]
        pulsePhases[i] = pulseTimes[i]-spikeTimes[precedingSpikeIndex]

    plt.plot(np.arange(start=1, stop=nPhases+1, step=1), pulsePhases,
                                                         marker=marker)
    plt.xlabel("pulse number, n")
    plt.ylabel(r'phase, $\theta_n$')
    plt.grid()

    for i in range(len(pulsePhases)):
        annotation = r"$\theta_{%d}$"%(i+1)
        plt.annotate(annotation, xy=(i+1, pulsePhases[i]), fontsize=fontsize)

    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

