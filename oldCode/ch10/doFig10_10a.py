
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
    resultsFilename = 'results/integrationINapIKFig10_10.npz'
    figFilename = 'figures/fig10_10a.eps'
    results = np.load(resultsFilename)

    plt.plot(results["times"], results["ys"][0,:], color="blue")
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane Potential (mV)")
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(results["times"], results["i"], color="lightgray")
    ax2.set_ylabel("Input Current (mA)")
    plt.savefig(figFilename)
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

