
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import malkinsHFunc

def main(argv):
    if len(argv)!=3:
        print("Usage: %s <i> <selfCouplingStrength>"%argv[0])
        sys.exit(1)

    i = int(argv[1])
    selfCouplingStrength = float(argv[2])
    i0 = 35.0
    paramLimitCycleFilename = "results/paramLimitCyclesINapIKLowThresholdI0%.02f.npz"%(i0)
    integrationQisFilename = "results/integrationQINapIKLowThresholdI0%.02f.npz"%(i0)
    malkinsWConstantFilename = "results/w%dINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02f.npz"%(i, selfCouplingStrength, i0)

    paramLimitCycleILoadRes = np.load(paramLimitCycleFilename)
    xsi = paramLimitCycleILoadRes["limitCycle"]
    xsiPhases = paramLimitCycleILoadRes["phases"]
    qsiIntRes = np.load(integrationQisFilename)
    qsiPhases = qsiIntRes["phases"]
    qsi = qsiIntRes["ys"]
    T = np.max(qsiIntRes["phases"])

    uncoupledFunc = lambda x1, x2: np.array([0.0, 0.0])
    selfCoupledFunc = lambda x1, x2: np.array([selfCouplingStrength*x1[0], 0.0])
    couplings = [selfCoupledFunc, uncoupledFunc]

    w = malkinsHFunc(qsi=qsi, qsiPhases=qsiPhases, 
                                xsi=xsi, xsiPhases=xsiPhases, 
                                xsj=xsi, xsjPhases=xsiPhases,
                                coupling=couplings[i], 
                                phaseDiff=0.0, T=T)
    print("w%d=%.02f"%(i, w))
    np.savez(file=malkinsWConstantFilename, w=w)

if __name__ == "__main__":
    main(sys.argv)

