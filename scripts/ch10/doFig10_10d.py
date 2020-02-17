
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from utils import getPeakIndices

def main(argv):
    nPhases = 6
    fontsize = 20
    marker = "o"
    integrationFilename = 'results/integrationINapIKFig10_10.npz'
    prcFilename = 'results/prcINapIKFig10_4RightPanel.npz'
    figFilename = 'figures/fig10_10d.eps'

    prcRes = np.load(prcFilename)
    integrationRes = np.load(integrationFilename)

    poincarePhaseMap = (prcRes["phases"]+prcRes["prc"]+integrationRes["Ts"])%prcRes["T"]

    plt.plot(prcRes["phases"], poincarePhaseMap)
    plt.plot(prcRes["phases"], prcRes["phases"])
    plt.xlabel(r"$\theta_n$")
    plt.ylabel(r"$\theta_{n+1}$")
    pulseTimes = integrationRes["offset"]+\
                  np.arange(start=0, stop=nPhases, step=1)*integrationRes["Ts"]

    spikeIndices = getPeakIndices(v=integrationRes["ys"][0,:])
    spikeTimes = integrationRes["times"][spikeIndices]

    pulsePhases = np.empty(pulseTimes.shape)
    for i in range(len(pulsePhases)):
        precedingSpikeIndex = np.nonzero(spikeTimes<pulseTimes[i])[0][-1]
        pulsePhases[i] = pulseTimes[i]-spikeTimes[precedingSpikeIndex]

    for i in range(len(pulsePhases)):
        annotation = r"$\theta_{%d}$"%(i+1)
        plt.annotate(annotation, xy=(pulsePhases[i], pulsePhases[i]), fontsize=fontsize)

    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

