
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
    epsilon = 0.1
    i0 = 10
    couplingStartTime = 99.04
    dt = 1e-2
    wiMarker = "x"
    integrationINapIKFilename = "results/integrationWCoupledINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    integrationQsFilename = "results/integrationQINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d.npz"%(i0, epsilon, couplingStartTime, i)
    malkinsWConstantFilename = "results/w%dINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(i, selfCouplingStrength, i0, epsilon, couplingStartTime)

    integrationINapIKRes = np.load(integrationINapIKFilename)
    iStartTimeIndex = np.argmin(np.abs(couplingStartTime-
                                       integrationINapIKRes["times%dUncoupled"%(i)]))
    xsiTimes = integrationINapIKRes["times%dUncoupled"%(i)][iStartTimeIndex:]-\
               integrationINapIKRes["times%dUncoupled"%(i)][iStartTimeIndex]
    xsi = integrationINapIKRes["ys%dUncoupled"%(i)][:,iStartTimeIndex:]
    qsIntRes = np.load(integrationQsFilename)
    qsTimes = qsIntRes["times"]
    qs = qsIntRes["ys"]
    T = np.max(qsIntRes["times"])

    uncoupledFunc = lambda x1, x2: np.array([0.0, 0.0])
    selfCoupledFunc = lambda x1, x2: np.array([selfCouplingStrength*x1[0], 0.0])
    couplings = [selfCoupledFunc, uncoupledFunc]

    w = malkinsHFunc(qs=qs, qsTimes=qsTimes, 
                            xsi=xsi, xsiTimes=xsiTimes, 
                            xsj=xsi, xsjTimes=xsiTimes,
                            coupling=couplings[i], 
                            phaseDiff=0.0, T=T)
    np.savez(file=malkinsWConstantFilename, w=w)

    plt.plot(w, marker=wiMarker)
    plt.grid()
    plt.axhline(y=0, color="gray")
    plt.xlabel("Phase Difference")
    plt.ylabel(r"$w_%d$"%(i))
    plt.legend()
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

