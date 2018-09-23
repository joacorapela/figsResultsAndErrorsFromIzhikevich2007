
import sys
import numpy as np
import pdb

def main(argv):
    if len(argv)!=2:
        print("Usage: %s <selfCouplingStrength>"%argv[0])
        sys.exit(1)

    selfCouplingStrength = float(argv[1])
    epsilon = 0.1
    i0 = 10
    couplingStartTime = 99.04
    malkinsWiConstantFilenamePattern = "results/w%dINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"
    malkinsWConstantFilename = "results/wINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)

    loadRes = np.load(malkinsWiConstantFilenamePattern%(0, selfCouplingStrength, i0, epsilon, couplingStartTime))
    w0 = loadRes["w"]

    loadRes = np.load(malkinsWiConstantFilenamePattern%(1, selfCouplingStrength, i0, epsilon, couplingStartTime))
    w1 = loadRes["w"]

    w = w1-w0

    np.savez(malkinsWConstantFilename, w=w)

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

