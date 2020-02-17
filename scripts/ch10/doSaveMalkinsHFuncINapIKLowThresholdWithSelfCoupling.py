
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import malkinsHFunc

def main(argv):
    epsilon = 0.01
    i0 = 35
    couplingStartTime = 100.44
    oldSelfCouplingStrength = 5.0
    selfCouplingStrength = -20.0
    # i = 1
    # j = 0
    # i = 0
    # j = 1
    i = 0
    j = 0
    # i = 1
    # j = 1
    dt = 1e-2
    hiiMarker = "x"
    integrationINapIKFilename = "results/integrationWCoupledINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(oldSelfCouplingStrength, i0, epsilon, couplingStartTime)
    integrationQsFilename = "results/integrationQINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d.npz"%(i0, epsilon, couplingStartTime, i)
    malkinsHFuncFilename = "results/h%d%dINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(i, j, selfCouplingStrength, i0, epsilon, couplingStartTime)

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

    uncoupledFunc = lambda x1, x2: np.array([0.0, 0.0])
    btwCoupledFunc = lambda x1, x2: np.array([x2[0]-x1[0], 0.0]) 
    selfCoupledFunc = lambda x1, x2: np.array([selfCouplingStrength*x1[0], 0.0])
    couplings = [[selfCoupledFunc, btwCoupledFunc], 
                 [btwCoupledFunc, uncoupledFunc]]

    if i==j:
        phaseDiffs = [0.0]
        hValues = [malkinsHFunc(qs=qs, qsTimes=qsTimes,
                                       xsi=xsi,
                                       xsiTimes=xsiTimes,
                                       xsj=xsj,
                                       xsjTimes=xsjTimes,
                                       couplings=couplings, 
                                       i=i, j=j, 
                                       phaseDiff=0.0,
                                       T=T)]
    else:
        phaseDiffs = np.arange(0, T, dt)
        hValues = np.empty(len(phaseDiffs))
        for k in xrange(len(phaseDiffs)):
            hValues[k] = malkinsHFunc(qs=qs, qsTimes=qsTimes,
                                             xsi=xsi,
                                             xsiTimes=xsiTimes,
                                             xsj=xsj,
                                             xsjTimes=xsjTimes,
                                             couplings=couplings, 
                                             i=i, j=j, 
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

