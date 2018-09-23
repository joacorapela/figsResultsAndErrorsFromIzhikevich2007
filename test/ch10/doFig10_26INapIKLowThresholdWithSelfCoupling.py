
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import malkinsHFunc

def main(argv):
    i0 = 35.0
    couplingStartTime = 100.44
    malkinsHFuncFilename = "results/hINapIKLowThresholdI0%.02f.npz"%(i0)
    figFilename = "figures/fig10_26INapIKLowThresholdI0%.02f.eps"%(i0)

    loadRes = np.load(malkinsHFuncFilename)
    phaseDiffs = loadRes["phaseDiffs"]
    hValues = loadRes["hValues"]

    gValues = np.empty(len(phaseDiffs))
    for k in xrange(len(phaseDiffs)):
        gValues[k] = hValues[-k]-hValues[k]

    plt.plot(phaseDiffs, hValues, label=r"$H_{ij}(\chi)$")
    plt.plot(phaseDiffs, gValues, label=r"$G(\chi)$")
    plt.axhline(y=0, color="lightgray")
    plt.xlabel(r"Phase Difference, $\chi$")
    plt.grid()
    plt.legend()
    plt.savefig(figFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

