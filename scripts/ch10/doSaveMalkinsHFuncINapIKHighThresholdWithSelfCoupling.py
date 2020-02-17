
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import malkinsHFunc

def main(argv):
    epsilon = 0.1
    i0 = 10
    couplingStartTime = 99.04
    selfCouplingStrength = 0.65
    i = 1
    j = 0
    # i = 0
    # j = 1
    dt = 1e-2
    integrationINapIKFilename = "results/integrationWCoupledINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    integrationQsFilename = "results/integrationQINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d.npz"%(i0, epsilon, couplingStartTime, i)
    malkinsHFuncFilename = "results/h%d%dINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(i, j, i0, epsilon, couplingStartTime)

    integrationINapIKRes = np.load(integrationINapIKFilename)
    iStartTimeIndex = np.argmin(np.abs(couplingStartTime-
                                       integrationINapIKRes["times%dUncoupled"%(i)]))
    xsiTimes = integrationINapIKRes["times%dUncoupled"%(i)][iStartTimeIndex:]-\
               integrationINapIKRes["times%dUncoupled"%(i)][iStartTimeIndex]
    xsi = integrationINapIKRes["ys%dUncoupled"%(i)][:,iStartTimeIndex:]
    jStartTimeIndex = np.argmin(np.abs(couplingStartTime-
                                       integrationINapIKRes["times%dUncoupled"%(j)]))
    xsjTimes = integrationINapIKRes["times%dUncoupled"%(j)][jStartTimeIndex:]-\
               integrationINapIKRes["times%dUncoupled"%(j)][jStartTimeIndex]
    xsj = integrationINapIKRes["ys%dUncoupled"%(i)][:,jStartTimeIndex:]
    qsIntRes = np.load(integrationQsFilename)
    qsTimes = qsIntRes["times"]
    qs = qsIntRes["ys"]
    T = np.max(qsIntRes["times"])

    btwCoupledFunc = lambda x1, x2: np.array([x2[0]-x1[0], 0.0]) 

    phaseDiffs = np.arange(0, T, dt)
    hValues = np.empty(len(phaseDiffs))
    for k in xrange(len(phaseDiffs)):
        hValues[k] = malkinsHFunc(qs=qs, qsTimes=qsTimes,
                                         xsi=xsi,
                                         xsiTimes=xsiTimes,
                                         xsj=xsj,
                                         xsjTimes=xsjTimes,
                                         coupling=btwCoupledFunc, 
                                         phaseDiff=phaseDiffs[k],
                                         T=T)
        print("h%d%dValues[phaseDiff=%.04f]=%.04f"%(i, j, phaseDiffs[k],
                                                           hValues[k]))
    np.savez(file=malkinsHFuncFilename, phaseDiffs=phaseDiffs, hValues=hValues)

    if len(hValues)>1:
        plt.plot(phaseDiffs, hValues, label=r"$H_{%d%d}$"%(i,j))
    else:
        plt.plot(phaseDiffs, hValues, marker=hiiMarker, label=r"$H_{%d%d}$"%(i,j))
    plt.grid()
    plt.axhline(y=0, color="gray")
    plt.xlabel("Phase Difference")
    plt.ylabel(r"$H_{ij}$")
    plt.legend()
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

