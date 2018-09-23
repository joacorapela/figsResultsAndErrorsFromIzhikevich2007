
import sys
import pdb
import numpy as np
import pdb
import matplotlib.pyplot as plt
import scipy.integrate as integrate

def main(argv):
    phaseDiff = 0.5
    epsilon = 0.003
    i0 = 35
    couplingStartTime = 100.44
    # i = 1
    # j = 0
    i = 0
    j = 1
    integrationINapIKFilename = "results/integrationWCoupledINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    integrationQisFilename = "results/integrationQINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f_oscillator%d.npz"%(i0, epsilon, couplingStartTime, i)

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
    qisIntRes = np.load(integrationQisFilename)
    qisTimes = qisIntRes["times"][::-1]
    qis0 = qisIntRes["ys"][0][::-1]
    T = np.max(qisIntRes["times"])

    dtXsj = np.mean(xsjTimes[1:]-xsjTimes[:-1])
    phaseDiffInSamples = int(phaseDiff/dtXsj)
    xsjShifted = xsj[:,phaseDiffInSamples:]
    xsjShiftedTrimmed = xsjShifted[0,:len(qisTimes)] 
    xiTrimmed = xsi[0,:len(qisTimes)]
    xiTrimmedTimes = xsiTimes[:len(qisTimes)]
    xsjShiftedTrimmedMinusXiTrimmed =  xsjShiftedTrimmed - xiTrimmed 
    dtQis = np.mean(qisTimes[1:]-qisTimes[:-1])
    intRes = np.sum(qis0*xsjShiftedTrimmedMinusXiTrimmed)*dtQis/T

    print("intRes=%02f"%(intRes))

    ax = plt.gca()
    ax.plot(qisTimes, xsjShiftedTrimmed, label="xj")
    ax.plot(xiTrimmedTimes, xiTrimmed, label="xi")
    ax.plot(xiTrimmedTimes, xsjShiftedTrimmedMinusXiTrimmed, label="xj-xi")
    ax.axhline(y=0, color="gray")
    ax2 = ax.twinx()
    ax2.plot(qisTimes, qis0, '--', label="qis0")
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")
    ax2.axhline(y=0, color="gray", linestyle="--")
    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

