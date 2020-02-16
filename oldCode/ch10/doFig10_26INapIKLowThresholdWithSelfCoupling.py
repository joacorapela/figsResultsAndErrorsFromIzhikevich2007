
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import malkinsHFunc

def main(argv):
    i0 = 35.0
    epsilon = 0.01
    couplingStartTime = 100.44
    malkinsHFuncFilenamePattern = "results/h%d%dINapIKLowThresholdWithSelfCouplingI0%.02fEpsilon%.06fCouplingStart%.02f.npz"
    figFilename = "figures/fig10_26INapIKLowThresholdWithSelfCouplingINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.eps"%(i0, epsilon, couplingStartTime)

    load01Res = np.load(malkinsHFuncFilenamePattern%(0, 1, i0, epsilon, 
                                                     couplingStartTime))
    phaseDiffs01 = load01Res["phaseDiffs"]
    hValues01 = load01Res["hValues"]

    load10Res = np.load(malkinsHFuncFilenamePattern%(1, 0, i0, epsilon, 
                                                     couplingStartTime))
    phaseDiffs10 = load10Res["phaseDiffs"]
    hValues10 = load10Res["hValues"]

    gValues = np.empty(len(phaseDiffs01))
    for k in xrange(len(phaseDiffs01)):
        gValues[k] = hValues10[-k]-hValues01[k]

    plt.plot(phaseDiffs01, hValues01, label=r"$H_{01}(\chi)$")
    plt.plot(phaseDiffs10, hValues10, label=r"$H_{10}(\chi)$")
    plt.plot(phaseDiffs01, gValues, label=r"$G(\chi)$")
    plt.axhline(y=0, color="lightgray")
    plt.xlabel(r"Phase Difference, $\chi$")
    plt.grid()
    plt.legend()
    plt.savefig(figFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

