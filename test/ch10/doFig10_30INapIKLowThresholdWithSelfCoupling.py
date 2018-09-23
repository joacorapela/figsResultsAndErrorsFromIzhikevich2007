
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
    i0 = 35.0
    malkinsWConstantFilename = "results/wINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02f.npz"%(selfCouplingStrength, i0)
    malkinsGFuncFilename = "results/gINapIKLowThresholdI0%.02f.npz"%(i0)
    figFilename = "figures/fig10_30INapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02f.eps"%(selfCouplingStrength, i0)

    loadRes = np.load(malkinsWConstantFilename)
    w = loadRes["w"]

    loadRes = np.load(malkinsGFuncFilename)
    phaseDiffs = loadRes["phaseDiffs"]
    gValues = loadRes["gValues"]

    figHandle = plt.figure()
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

