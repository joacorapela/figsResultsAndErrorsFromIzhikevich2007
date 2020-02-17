
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from MalkinsPhaseDeviationModelOfWeaklyCoupledOscillators import MalkinsPhaseDeviationModelOfWeaklyCoupledOscillators 
from syncUtils import getPhasesFromVoltages
from utils import integrateForward

def main(argv):
    epsilon = 0.1
    i0 = 10
    couplingStartTime = 99.04
    duration = 100.0
    dt = 1e-2
    integrationWCOsFilename = "results/integrationWCoupledINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    hFilenamePattern = "results/h%d%dINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.npz"
    resultsFilename = "results/integrationPhasesDifferencesINapIKHighThresholdI0%.02fEpsilon%.05fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)

    integrationWCOs = np.load(integrationWCOsFilename)

    def h(phaseDiff, phaseDiffs, hs, i, j):
        T = np.max(phaseDiffs)
        wrappedPhaseDiff = phaseDiff%T
        phaseDiffIndex = np.argmin(np.abs(wrappedPhaseDiff-phaseDiffs))
        answer = hs[phaseDiffIndex]
        print("h%d%d[phaseDiff=%.04f]=%.04f"%(i, j, wrappedPhaseDiff, answer))
        # plt.plot(phaseDiffs, hs); plt.title("h%d%d(%f)=%f"%(i, j, wrappedPhaseDiff, answer)); plt.axvline(x=wrappedPhaseDiff, color="gray"); plt.show()
        # pdb.set_trace()
        return(answer)

    h01IntRes = np.load(hFilenamePattern%(0, 1, i0, epsilon, couplingStartTime))
    h01 = lambda phaseDiff: h(i=0, j=1, phaseDiff=phaseDiff,
                               phaseDiffs=h01IntRes["phaseDiffs"],
                               hs=h01IntRes["hValues"])
    h10IntRes = np.load(hFilenamePattern%(1, 0, i0, epsilon, couplingStartTime))
    h10 = lambda phaseDiff: h(i=1, j=0, phaseDiff=phaseDiff,
                               phaseDiffs=h10IntRes["phaseDiffs"],
                               hs=h10IntRes["hValues"])
    zeroH = lambda phaseDiff: 0.0
    hs = [[zeroH, h01], [h10, zeroH]]

    pdModel = MalkinsPhaseDeviationModelOfWeaklyCoupledOscillators(hs=hs, 
                                                                    epsilon=
                                                                     epsilon)

    timesNeuron0 = integrationWCOs["times0Uncoupled"]
    voltagesNeuron0 = integrationWCOs["ys0Uncoupled"][0,:]
    resPhasesNeuron0 = getPhasesFromVoltages(times=timesNeuron0, voltages=voltagesNeuron0)
    phasesNeuron0 = resPhasesNeuron0["phases"]
    timePhasesNeuron0 = resPhasesNeuron0["times"]
    index = np.argmin(np.abs(couplingStartTime+0.05-timePhasesNeuron0))
    phaseNeuron0AtCouplingStartTime = phasesNeuron0[index]

    timesNeuron1 = integrationWCOs["times1Uncoupled"]
    voltagesNeuron1 = integrationWCOs["ys1Uncoupled"][0,:]
    resPhasesNeuron1 = getPhasesFromVoltages(times=timesNeuron1, voltages=voltagesNeuron1)
    phasesNeuron1 = resPhasesNeuron1["phases"]
    timePhasesNeuron1 = resPhasesNeuron1["times"]
    index = np.argmin(np.abs(couplingStartTime+0.05-timePhasesNeuron1))
    phaseNeuron1AtCouplingStartTime = phasesNeuron1[index]

    y0 = [phaseNeuron0AtCouplingStartTime, phaseNeuron1AtCouplingStartTime]
    t0 = couplingStartTime
    tf = t0+duration
    nTSteps = int((tf-t0)/dt)
    intRes = integrateForward(deriv=pdModel.deriv, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
    np.savez(resultsFilename, times=intRes["times"], ys=intRes["ys"])

    ax1= plt.subplot(2, 1, 1)
    plt.plot(integrationWCOs["times0Uncoupled"], integrationWCOs["ys0Uncoupled"][0,:], color="red", label=r"$V_0$")
    plt.plot(integrationWCOs["times1Uncoupled"], integrationWCOs["ys1Uncoupled"][0,:], color="blue", label=r"$V_1$")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane\nPotential (mV)")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend(loc="upper left")

    ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    plt.plot(intRes["times"], intRes["ys"][0, :], color="red", label=r"$\phi_0$")
    plt.plot(intRes["times"], intRes["ys"][1, :], color="blue", label=r"$\phi_1$")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Phase Deviation")
    plt.legend(loc="upper left")

    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

