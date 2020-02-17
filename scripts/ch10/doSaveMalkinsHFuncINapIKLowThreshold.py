
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import malkinsHFunc

def main(argv):
    epsilon = 0.003
    i0 = 35.0
    couplingStartTime = 100.44
    # i = 0
    # j = 1
    i = 1
    j = 0
    dt = 1e-2
    integrationINapIKFilename = "results/integrationWCoupledINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    integrationQisFilename = "results/integrationQINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d.npz"%(i0, epsilon, couplingStartTime, i)
    malkinsHFuncFilename = "results/h%d%dINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.npz"%(i, j, i0, epsilon, couplingStartTime)

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
    xsj = integrationINapIKRes["ys%dUncoupled"%(j)][:,jStartTimeIndex:]
    qsiIntRes = np.load(integrationQisFilename)
    qsiTimes = qsiIntRes["times"]
    qsi = qsiIntRes["ys"]
    T = np.max(qsiIntRes["times"])

    # begin debug
    # xi0Trimmed = xsi[0,:len(qsiTimes)]
    # xj0Trimmed = xsj[0,:len(qsiTimes)]
    # plt.plot(qsiTimes, xi0Trimmed, label="i")
    # plt.plot(qsiTimes, xj0Trimmed, label="j")
    # plt.legend()
    # plt.show()
    # end debug

    phaseDiffs = np.arange(0, T, dt)
    uncoupledFunc = lambda x1, x2: np.array([0.0, 0.0])
    coupledFunc = lambda x1, x2: np.array([x2[0]-x1[0], 0.0])
    couplings = [[uncoupledFunc, coupledFunc], 
                 [coupledFunc, uncoupledFunc]]
    hValues = np.empty(len(phaseDiffs))
    for k in xrange(len(phaseDiffs)):
        hValues[k] = malkinsHFunc(qsi=qsi, qsiTimes=qsiTimes,
                                           xsi=xsi,
                                           xsiTimes=xsiTimes,
                                           xsj=xsj,
                                           xsjTimes=xsjTimes,
                                           coupling=couplings[i][j],
                                           phaseDiff=phaseDiffs[k],
                                           T=T)
        print("h%d%dValues[phaseDiff=%.04f]=%.04f"%(i, j, 
                                                       phaseDiffs[k], 
                                                       hValues[k]))
    np.savez(file=malkinsHFuncFilename, phaseDiffs=phaseDiffs, hValues=hValues)

    plt.plot(phaseDiffs, hValues, label=r"$H_{%d%d}$"%(i,j))
    plt.axhline(y=0, color="gray")
    plt.xlabel("Phase Difference")
    plt.ylabel(r"$H_{ij}$")
    plt.legend()
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

