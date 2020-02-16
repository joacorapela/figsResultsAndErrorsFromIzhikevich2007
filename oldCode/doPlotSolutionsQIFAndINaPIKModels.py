

import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    if len(argv)!=3:
        sys.exit("Usage: %s tauV i0"%argv[0])
    tauV = float(argv[1])
    i0 = float(argv[2])
    qifResultsFilename = 'results/quadraticIFSolutionI%.02f.npz'%i0
    iNapIKResultsFilename = 'results/integrationINapIKFig6-07TauV%.02fI%.02f.npz'%(tauV,i0)
    figFilename = 'figures/qIFAndINapIKSolutionsTauV%.02fI%.02f.eps'%(tauV,i0)

    qifResults = np.load(qifResultsFilename)
    iNapIKResults = np.load(iNapIKResultsFilename)

    plt.plot(qifResults['times'], qifResults['vs'], label="QIF")
    plt.plot(iNapIKResults['times'], iNapIKResults['ys'][0,:], label="INapIK")
    axes = plt.gca()
    ylim = axes.get_ylim()
    axes.set_ylim((ylim[0], ylim[1]*1.1))
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Voltage (mV)")
    plt.legend()
    plt.grid()
    plt.savefig(figFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

