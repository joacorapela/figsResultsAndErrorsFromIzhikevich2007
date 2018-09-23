
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import malkinsHFunc

def main(argv):
    i0 = 35
    dt = 1e-2
    paramLimitCycleIFilename = "results/paramLimitCyclesINapIKLowThresholdI0%.02f.npz"%(i0)
    paramLimitCycleJFilename = "results/paramLimitCyclesINapIKLowThresholdI0%.02f.npz"%(i0)
    integrationQisFilename = "results/integrationQINapIKLowThresholdI0%.02f.npz"%(i0)
    malkinsHFuncFilename = "results/hNapIKLowThresholdWithI0%.02f.npz"%(i0)

    paramLimitCycleILoadRes = np.load(paramLimitCycleIFilename)
    xsi = paramLimitCycleILoadRes["limitCycle"]
    xsiPhases = paramLimitCycleILoadRes["phases"]
    paramLimitCycleJLoadRes = np.load(paramLimitCycleJFilename)
    xsj = paramLimitCycleJLoadRes["limitCycle"]
    xsjPhases = paramLimitCycleJLoadRes["phases"]

    qsiIntRes = np.load(integrationQisFilename)
    qsiPhases = qsiIntRes["phases"]
    qsi = qsiIntRes["ys"]
    T = np.max(qsiPhases)

    btwCoupledFunc = lambda x1, x2: np.array([x2[0]-x1[0], 0.0]) 

    phaseDiffs = np.arange(0, T, dt)
    hValues = np.empty(len(phaseDiffs))
    for k in xrange(len(phaseDiffs)):
        hValues[k] = malkinsHFunc(qsi=qsi, qsiPhases=qsiPhases,
                                           xsi=xsi,
                                           xsiPhases=xsiPhases,
                                           xsj=xsj,
                                           xsjPhases=xsjPhases,
                                           coupling=btwCoupledFunc,
                                           phaseDiff=phaseDiffs[k],
                                           T=T)
        print("hValues[phaseDiff=%.04f]=%.04f"%(phaseDiffs[k], hValues[k]))
    np.savez(file=malkinsHFuncFilename, phaseDiffs=phaseDiffs, hValues=hValues)

    plt.plot(phaseDiffs, hValues)
    plt.grid()
    plt.axhline(y=0, color="gray")
    plt.xlabel("Phase Difference")
    plt.ylabel(r"$H_{ij}$")
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

