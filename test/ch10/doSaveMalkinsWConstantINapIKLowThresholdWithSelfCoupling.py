
import sys
import numpy as np
import pdb

def main(argv):
    if len(argv)!=2:
        print("Usage: %s <selfCouplingStrength>"%argv[0])
        sys.exit(1)

    selfCouplingStrength = float(argv[1])
    i0 = 35.0
    malkinsWiConstantFilenamePattern = "results/w%dINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02f.npz"
    malkinsWConstantFilename = "results/wINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02f.npz"%(selfCouplingStrength, i0)

    loadRes = np.load(malkinsWiConstantFilenamePattern%(0, selfCouplingStrength, i0))
    w0 = loadRes["w"]

    loadRes = np.load(malkinsWiConstantFilenamePattern%(1, selfCouplingStrength, i0))
    w1 = loadRes["w"]

    w = w1-w0

    np.savez(malkinsWConstantFilename, w=w)

    print("w=%.02f"%(w))

    # pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

