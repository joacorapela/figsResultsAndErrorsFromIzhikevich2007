
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
# import dill
from syncUtils import malkinsHFunc

def main(argv):
    if len(argv)!=2:
        print("Usage: %s <selfCouplingStrength>"%argv[0])
        sys.exit(1)

    selfCouplingStrength = float(argv[1])
    epsilon = 0.1
    i0 = 10
    couplingStartTime = 99.04
    malkinsWConstantFilename = "results/wINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    malkinsGFuncFilename = "results/gINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    figFilename = "figures/fig10_30INapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.eps"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    figPickleFilename = "results/fig10_30INapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.pkl"%(selfCouplingStrength, i0, epsilon, couplingStartTime)

    loadRes = np.load(malkinsWConstantFilename)
    w = loadRes["w"]

    loadRes = np.load(malkinsGFuncFilename)
    phaseDiffs = loadRes["phaseDiffs"]
    gValues = loadRes["gValues"]

    figHandle = plt.figure()
    # plt.plot(phaseDiffs01, hValues01, label=r"$H_{01}(\chi)$")
    # plt.plot(phaseDiffs10, hValues10, label=r"$H_{10}(\chi)$")
    plt.plot(phaseDiffs, gValues, label=r"$G(\chi)$")
    plt.axhline(y=-w, linestyle="dashed", color="orange", label="-w")

    plt.axhline(y=0, color="lightgray")
    plt.xlabel(r"Phase Difference, $\chi$")
    plt.grid()
    plt.legend()
    plt.savefig(figFilename)

    # output = open(figPickleFilename, "w")
    # dill.dumps(figHandle, output)
    # output.close()

    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

