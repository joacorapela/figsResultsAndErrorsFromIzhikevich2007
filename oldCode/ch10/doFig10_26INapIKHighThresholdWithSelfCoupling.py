
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import malkinsHFunc

def main(argv):
    i0 = 10
    epsilon = 0.1
    couplingStartTime = 99.04
    i = 0
    j = 1
    malkinsHFuncFilename = "results/h%d%dINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(i, j, i0, epsilon, couplingStartTime)
    figFilename = "figures/fig10_26INapIKHighThresholdh%d%dINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.eps"%(i, j, i0, epsilon, couplingStartTime)

    loadRes = np.load(malkinsHFuncFilename)
    phaseDiffs = loadRes["phaseDiffs"]
    hValues = loadRes["hValues"]

    gValues = np.empty(len(phaseDiffs))
    for k in xrange(len(phaseDiffs)):
        gValues[k] = hValues[-k]-hValues[k]

    plt.plot(phaseDiffs, hValues, label=r"H($\chi$)")
    plt.plot(phaseDiffs, gValues, label=r"G($\chi$)")
    plt.axhline(y=0, color="lightgray")
    plt.xlabel(r"Phase Difference, $\chi$")
    plt.legend()
    plt.savefig(figFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

