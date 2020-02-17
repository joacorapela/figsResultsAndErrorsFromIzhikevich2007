
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
    resultsFilename = 'results/prcINapIKFig10_4RightPanel.npz'
    figFilename = 'figures/fig10_4RightPanel.eps'
    prcRes = np.load(resultsFilename)
    plt.plot(prcRes['phases'], prcRes['prc'], marker="o")
    plt.xlabel("Phase (ms)")
    plt.ylabel("Phase Reset (ms)")
    plt.savefig(figFilename)
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

