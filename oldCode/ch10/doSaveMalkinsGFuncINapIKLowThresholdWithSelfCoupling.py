
import sys
import numpy as np
import pdb

def main(argv):
    if len(argv)!=2:
        print("Usage: %s <selfCouplingStrength>"%argv[0])
        sys.exit(1)

    selfCouplingStrength = float(argv[1])
    epsilon = 0.003
    i0 = 35.00
    couplingStartTime = 100.44
    malkinsHFuncFilenamePattern = "results/h%d%dINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.npz"
    malkinsWiConstantFilenamePattern = "results/w%dINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"
    malkinsGFuncFilename = "results/gINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)

    loadRes = np.load(malkinsWiConstantFilenamePattern%(0, selfCouplingStrength, i0, epsilon, couplingStartTime))
    w0 = loadRes["w"]

    loadRes = np.load(malkinsWiConstantFilenamePattern%(1, selfCouplingStrength, i0, epsilon, couplingStartTime))
    w1 = loadRes["w"]

    loadRes = np.load(malkinsHFuncFilenamePattern%(0, 1, i0, epsilon, couplingStartTime))
    phaseDiffs01 = loadRes["phaseDiffs"]
    hValues01 = loadRes["hValues"]

    loadRes = np.load(malkinsHFuncFilenamePattern%(1, 0, i0, epsilon, couplingStartTime))
    phaseDiffs10 = loadRes["phaseDiffs"]
    hValues10 = loadRes["hValues"]

    gValues = np.empty(len(phaseDiffs01))
    for k in xrange(len(phaseDiffs01)):
        gValues[k] = hValues10[-k]-hValues01[k]

    np.savez(malkinsGFuncFilename, phaseDiffs=phaseDiffs01, gValues=gValues)

    # pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

