
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
    Ts = 3.403
    resultsFilename = 'results/prcINapIKFig10_4RightPanel_INapIKLowThreshold.npz'
    figFilename = 'figures/fig10_4RightPanel_INapIKLowThreshold.eps'

    prcRes = np.load(resultsFilename)

    prc = prcRes['prc']
    phases = prcRes['phases']
    dPhase = phases[1]-phases[0]
    dPRC = np.empty(len(prc))
    dPRC[1:] = (prc[1:]-prc[:-1])/dPhase
    dPRC[0] = (prc[0]-prc[-1])/dPhase

    plt.plot(prcRes['phases'], prcRes['prc'], color="blue", marker="o")
    plt.axhline(y=prcRes['T']-Ts, color="blue", linestyle="solid")
    plt.xlabel("Phase (ms)")
    plt.ylabel("Phase Reset (ms)")
    plt.grid()
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(phases, dPRC, color="magenta", marker="o")
    ax2.set_ylabel("Derivative")
    ax2.axhline(y=0, color="magenta", linestyle="dotted")
    plt.savefig(figFilename)
    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

