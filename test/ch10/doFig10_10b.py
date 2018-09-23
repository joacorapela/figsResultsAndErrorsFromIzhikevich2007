
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from plotFunctions import plotHighThresholdINapIKVectorField

def main(argv):
    results10_4Filename = 'results/integrationINapIKFig10_4LeftPanel.npz'
    results10_10Filename = 'results/integrationINapIKFig10_10.npz'
    figFilename = 'figures/fig10_10b.eps'
    nPhases = 4
    ylim = (-.1, .7)
    fontsize = 20

    results10_4 = np.load(results10_4Filename)
    results10_10 = np.load(results10_10Filename)

    plt.plot(results10_10["ys"][0,:], results10_10["ys"][1,:], label="limit cycle pulse")
    plt.plot(results10_4["ysDC"][0,:], results10_4["ysDC"][1,:], label="limit cycle DC")
    plotHighThresholdINapIKVectorField(i=results10_10["i0"])
    plt.xlabel("Membrane Potential (V)")
    plt.ylabel('K activation variable, n')
    plt.ylim(ylim)

    pulseTimes = results10_10["offset"]+\
                  np.arange(start=0, stop=nPhases, step=1)*results10_10["Ts"]

    pulseIndices = np.empty(pulseTimes.shape)
    for i in range(len(pulseIndices)):
        pulseIndices[i] = np.argmin(np.abs(pulseTimes[i]-results10_10["times"]))

    for i in range(len(pulseIndices)):
        annotation = r"$\theta_%d$"%(i+1)
        plt.annotate(annotation, 
                      xy=(results10_10["ys"][0, pulseIndices[i]], 
                           results10_10["ys"][1, pulseIndices[i]]),
                      fontsize=fontsize)
    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

