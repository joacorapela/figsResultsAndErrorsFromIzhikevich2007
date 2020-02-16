
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):

    resultsFilename= 'results/integrationINapIKFig4-29.npz'
    figFilename = 'figures/fig4-29.eps'

    results = np.load(resultsFilename)
    ys = results["ys"]
    times = results["times"]
    currents = results["currents"]

    plt.subplot(2, 1, 1)
    plt.plot(times, ys[0,:])
    plt.ylabel('Voltage (mv)')
    plt.subplot(2, 1, 2)
    plt.plot(times, currents)
    plt.ylabel('Current')
    plt.xlabel('Time (ms)')
    plt.savefig(figFilename)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

