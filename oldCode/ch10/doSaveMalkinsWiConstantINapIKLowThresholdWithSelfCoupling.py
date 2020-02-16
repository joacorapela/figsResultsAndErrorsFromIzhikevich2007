
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
    epsilon = 0.003
    i0 = 35.0
    couplingStartTime = 100.44
    dt = 1e-3
    wiMarker = "x"
    integrationINapIKFilename = "results/integrationWCoupledINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    integrationQsiFilename = "results/integrationQINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d.npz"%(i0, epsilon, couplingStartTime, i)
    malkinsWConstantFilename = "results/w%dINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(i, selfCouplingStrength, i0, epsilon, couplingStartTime)

    integrationINapIKRes = np.load(integrationINapIKFilename)
    iStartTimeIndex = np.argmin(np.abs(couplingStartTime-
                                       integrationINapIKRes["times%dUncoupled"%(i)]))
    xsiTimes = integrationINapIKRes["times%dUncoupled"%(i)][iStartTimeIndex:]-\
               integrationINapIKRes["times%dUncoupled"%(i)][iStartTimeIndex]
    xsi = integrationINapIKRes["ys%dUncoupled"%(i)][:,iStartTimeIndex:]
    qsiIntRes = np.load(integrationQsiFilename)
    qsiTimes = qsiIntRes["times"]
    qsi = qsiIntRes["ys"]
    T = np.max(qsiIntRes["times"])

    uncoupledFunc = lambda x1, x2: np.array([0.0, 0.0])
    selfCoupledFunc = lambda x1, x2: np.array([selfCouplingStrength*x1[0], 0.0])
    couplings = [selfCoupledFunc, uncoupledFunc]

    w = malkinsHFunc(qsi=qsi, qsiTimes=qsiTimes, 
                                xsi=xsi, xsiTimes=xsiTimes, 
                                xsj=xsi, xsjTimes=xsiTimes,
                                coupling=couplings[i], 
                                phaseDiff=0.0, T=T)
    np.savez(file=malkinsWConstantFilename, w=w)

    # plt.plot(w, marker=wiMarker)
    # plt.grid()
    # plt.axhline(y=0, color="gray")
    # plt.xlabel("Phase Difference")
    # plt.ylabel(r"$w_%d$"%(i))
    # plt.legend()
    # plt.show()

    # pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

