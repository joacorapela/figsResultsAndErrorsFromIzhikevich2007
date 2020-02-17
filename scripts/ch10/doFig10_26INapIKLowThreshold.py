
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    i0 = 35.0
    epsilon = 0.003
    couplingStartTime = 100.44
    malkinsHFuncFilenamePattern = "results/h%d%dINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.npz"
    figFilename = "figures/fig10_26INapIKLowThresholdhINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.eps"%(i0, epsilon, couplingStartTime)

    h01Filename = malkinsHFuncFilenamePattern%(0, 1, i0, epsilon, couplingStartTime)
    h10Filename = malkinsHFuncFilenamePattern%(1, 0, i0, epsilon, couplingStartTime)
    loadRes = np.load(h01Filename)
    h01PhaseDiffs = loadRes["phaseDiffs"]
    h01Values = loadRes["hValues"]

    loadRes = np.load(h10Filename)
    h10PhaseDiffs = loadRes["phaseDiffs"]
    h10Values = loadRes["hValues"]

    gValues = np.empty(len(h01PhaseDiffs))
    for k in xrange(len(gValues)):
        gValues[k] = h10Values[-k]-h01Values[k]

    plt.plot(h01PhaseDiffs, h01Values, label=r"H($\chi$)")
    plt.plot(h01PhaseDiffs, gValues, label=r"G($\chi$)")
    plt.axhline(y=0, color="lightgray")
    plt.xlabel(r"Phase Difference, $\chi$")
    plt.grid()
    plt.legend()
    plt.savefig(figFilename)
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

