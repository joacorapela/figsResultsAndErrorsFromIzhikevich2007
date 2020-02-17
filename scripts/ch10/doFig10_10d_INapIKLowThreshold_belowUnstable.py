
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from utils import getPeakIndices

def main(argv):
    fontsize = 20
    marker = "o"
    integrationFilename = 'results/integrationINapIKFig10_10_INapIKLowThreshold_belowUnstable.npz'
    prcFilename = 'results/prcINapIKFig10_4RightPanel_INapIKLowThreshold.npz'
    figFilename = 'figures/fig10_10d_INapIKLowThreshold_belowUnstable.eps'

    prcRes = np.load(prcFilename)
    integrationRes = np.load(integrationFilename)

    poincarePhaseMap = (prcRes["phases"]+prcRes["prc"]+integrationRes["Ts"])%prcRes["T"]

    plt.plot(prcRes["phases"], poincarePhaseMap, marker="o")
    plt.plot(prcRes["phases"], prcRes["phases"], marker="o")
    plt.xlabel(r"$\theta_n$")
    plt.ylabel(r"$\theta_{n+1}$")
    # plt.xlim((0, .9))
    # plt.ylim((0, .9))
    spikeIndices = getPeakIndices(v=integrationRes["ysDCTrainPulses"][0,:])
    spikeTimes = integrationRes["timesDCTrainPulses"][spikeIndices]

    pulseTimes = np.arange(start=integrationRes["tPulse"], stop=spikeTimes[-1], step=integrationRes["Ts"])

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

