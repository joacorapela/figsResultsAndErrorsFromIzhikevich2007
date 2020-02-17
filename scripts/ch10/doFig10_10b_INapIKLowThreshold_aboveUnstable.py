
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from utils import getPeakIndices
from plotFunctions import plotLowThresholdINapIKVectorField

def main(argv):
    integrationFilename = 'results/integrationINapIKFig10_10_INapIKLowThreshold_aboveUnstable.npz'
    figFilename = 'figures/fig10_10b_INapIKLowThreshold_aboveUnstable.eps'
    nPhases = 6
    ylim = (-.1, .7)
    fontsize = 20

    integrationRes = np.load(integrationFilename)

    plt.plot(integrationRes["ysDCTrainPulses"][0,:],
              integrationRes["ysDCTrainPulses"][1,:], label="train pulses")
    plt.plot(integrationRes["ysDC"][0,:], integrationRes["ysDC"][1,:], label="DC")
    plotLowThresholdINapIKVectorField(i=integrationRes["i0"])
    plt.xlabel("Membrane Potential (V)")
    plt.ylabel('K activation variable, n')
    plt.ylim(ylim)

    spikeIndices = getPeakIndices(v=integrationRes["ysDCTrainPulses"][0,:])
    spikeTimes = integrationRes["timesDCTrainPulses"][spikeIndices]

    pulseTimes = np.arange(start=integrationRes["tPulse"],
                            stop=spikeTimes[-1], step=integrationRes["Ts"])

    pulseIndices = np.empty(pulseTimes.shape)
    for i in range(len(pulseIndices)):
        pulseIndices[i] = np.argmin(np.abs(pulseTimes[i]-integrationRes["timesDCTrainPulses"]))

    for i in range(len(pulseIndices)):
        annotation = r"$\theta_{%d}$"%(i+1)
        plt.annotate(annotation, 
                      xy=(integrationRes["ysDCTrainPulses"][0, pulseIndices[i]], 
                           integrationRes["ysDCTrainPulses"][1, pulseIndices[i]]),
                      fontsize=fontsize)
    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

