
import sys
import numpy as np
import pdb

def main(argv):
    i0 = 35.00
    malkinsHFuncFilename = "results/hINapIKLowThresholdI0%.02f.npz"%(i0)
    malkinsGFuncFilename = "results/gINapIKLowThresholdI0%.02f.npz"%(i0)


    loadRes = np.load(malkinsHFuncFilename)
    hPhaseDiffs = loadRes["phaseDiffs"]
    hValues = loadRes["hValues"]

    gValues = np.empty(len(hPhaseDiffs))
    for k in xrange(len(hPhaseDiffs)):
        gValues[k] = hValues[-k]-hValues[k]

    np.savez(malkinsGFuncFilename, phaseDiffs=hPhaseDiffs, gValues=gValues)

    # pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

