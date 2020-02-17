
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from utils import getPeakIndices

def main(argv):
    integrationFilename = 'results/integrationINapIKFig10_10_INapIKLowThreshold_belowUnstable.npz'
    prcFilename = 'results/prcINapIKFig10_4RightPanel_INapIKLowThreshold.npz'
    figFilename = 'figures/fig10_10c_INapIKLowThreshold_belowUnstable.eps'
    fontsize = 20
    marker = "o"

    integrationRes = np.load(integrationFilename)
    prcRes = np.load(prcFilename)

    spikeIndices = getPeakIndices(v=integrationRes["ysDCTrainPulses"][0,:])
    spikeTimes = integrationRes["timesDCTrainPulses"][spikeIndices]

    pulseTimes = np.arange(start=integrationRes["tPulse"],
                            stop=spikeTimes[-1], step=integrationRes["Ts"])

    pulsePhases = np.empty(pulseTimes.shape)
    for i in range(len(pulsePhases)):
        precedingSpikeIndex = np.nonzero(spikeTimes<pulseTimes[i])[0][-1]
        pulsePhases[i] = pulseTimes[i]-spikeTimes[precedingSpikeIndex]
        # if pulsePhases[i]>prcRes["T"]:
        #     pdb.set_trace()

    plt.plot(np.arange(start=1, stop=len(pulseTimes)+1, step=1), pulsePhases,
                                                         marker=marker)
    plt.axhline(y=prcRes["T"], color="red")
    plt.xlabel("pulse number, n")
    plt.ylabel(r'phase, $\theta_n$')
    plt.grid()

    # for i in range(len(pulsePhases)):
    #     annotation = r"$\theta_{%d}$"%(i+1)
    #     plt.annotate(annotation, xy=(i+1, pulsePhases[i]), fontsize=fontsize)

    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

