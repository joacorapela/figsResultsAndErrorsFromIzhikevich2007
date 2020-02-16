

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    resultsFilename = 'results/quadraticIFSolution.npz'
    figFilename = 'figures/quadraticIFSolution.eps'

    results = np.load(resultsFilename)

    plt.plot(results['times'], results['vs'])
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Voltage (mV)")
    plt.grid()
    plt.savefig(figFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

