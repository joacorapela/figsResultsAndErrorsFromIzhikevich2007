
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from MalkinsPhaseDeviationModelOfWeaklyCoupledOscillators import MalkinsPhaseDeviationModelOfWeaklyCoupledOscillators 
from syncUtils import getPhasesFromVoltages
from utils import computeLimitCycleAmplitudeAndPeriod

def main(argv):
    def integrateForwardModT(deriv, t0, y0, dt, T, nTSteps):
        times = np.arange(t0, t0+nTSteps*dt, dt)
        ys = np.empty((len(y0), len(times)))
        ys[:,0] = y0
        for i in np.arange(1, len(times)):
            ys[:,i] = (ys[:,i-1] + dt*deriv(y=ys[:,i-1], t=times[i-1]))%T
        return {"times":times, "ys":ys}

    epsilon = 0.01
    i0 = 35
    couplingStartTime = 100.44
    oscillatorIndex = 0
    duration = 400.0
    dt = 1e-3
    colorNeuron0 = "blue"
    colorNeuron1 = "green"
    linestyleCoupled = "-"
    linestyleUncoupled = ":"
    integrationWCOsFilename = "results/integrationWCoupledINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    hFilenamePattern = "results/h%d%dINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStart%.02f.npz"
    resultsFilename = "results/integrationPhasesDifferencesINapIKLowThresholdI0%.02fEpsilon%.05fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)

    integrationWCOs = np.load(integrationWCOsFilename)

    xs = integrationWCOs["ys%dUncoupled"%(oscillatorIndex)]
    times = integrationWCOs["times%dUncoupled"%(oscillatorIndex)]
    T = computeLimitCycleAmplitudeAndPeriod(xs=xs[0,:], times=times)["period"]

    def h(phaseDiff, phaseDiffs, hs, i, j):
        T = np.max(phaseDiffs)
        wrappedPhaseDiff = phaseDiff%T
        phaseDiffIndex = np.argmin(np.abs(wrappedPhaseDiff-phaseDiffs))
        answer = hs[phaseDiffIndex]
        # print("h%d%d[phaseDiff=%.04f]=%.04f"%(i, j, wrappedPhaseDiff, answer))
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
    index = np.argmin(np.abs(couplingStartTime-timePhasesNeuron0))
    phaseNeuron0AtCouplingStartTime = phasesNeuron0[index]

    timesNeuron1 = integrationWCOs["times1Uncoupled"]
    voltagesNeuron1 = integrationWCOs["ys1Uncoupled"][0,:]
    resPhasesNeuron1 = getPhasesFromVoltages(times=timesNeuron1, voltages=voltagesNeuron1)
    phasesNeuron1 = resPhasesNeuron1["phases"]
    timePhasesNeuron1 = resPhasesNeuron1["times"]
    index = np.argmin(np.abs(couplingStartTime-timePhasesNeuron1))
    phaseNeuron1AtCouplingStartTime = phasesNeuron1[index]

    y0 = [phaseNeuron0AtCouplingStartTime, phaseNeuron1AtCouplingStartTime]
    t0 = couplingStartTime
    tf = t0+duration
    nTSteps = int((tf-t0)/dt)
    intRes = integrateForwardModT(deriv=pdModel.deriv, t0=t0, y0=y0, dt=dt,
                                                       T=T, nTSteps=nTSteps)
    np.savez(resultsFilename, times=intRes["times"], ys=intRes["ys"])

    timesCoupled = integrationWCOs["timesCoupled"]
    voltagesCoupledNeuron0 = integrationWCOs["ysCoupled"][0,:]
    voltagesCoupledNeuron1 = integrationWCOs["ysCoupled"][2,:]
    voltagesUncoupledNeuron0 = integrationWCOs["ys0Uncoupled"][0,:]
    timesUncoupledNeuron0 = integrationWCOs["times0Uncoupled"]
    voltagesUncoupledNeuron1 = integrationWCOs["ys1Uncoupled"][0,:]
    timesUncoupledNeuron1 = integrationWCOs["times1Uncoupled"]

    ax1 = plt.subplot(2, 1, 1)
    plt.plot(timesCoupled, voltagesCoupledNeuron0, color=colorNeuron0,
                    linestyle=linestyleCoupled, label=r"coupled $V_0$")
    plt.plot(timesCoupled, voltagesCoupledNeuron1, color=colorNeuron1,
                    linestyle=linestyleCoupled, label=r"coupled $V_1$")
    plt.plot(timesUncoupledNeuron0, voltagesUncoupledNeuron0, 
                                    color=colorNeuron0,
                                    linestyle=linestyleUncoupled, 
                                    label=r"uncoupled $V_0$")
    plt.plot(timesUncoupledNeuron1, voltagesUncoupledNeuron1, 
                                    color=colorNeuron1,
                                    linestyle=linestyleUncoupled, 
                                    label=r"uncoupled $V_1$")
    plt.grid()
    plt.ylabel("Membrane\nPotential (mV)")
    plt.legend()
    plt.axvline(x=couplingStartTime, color="red")
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    plt.plot(intRes["times"], intRes["ys"][0, :], color=colorNeuron0,
                              label=r"$\varphi_0$")
    plt.plot(intRes["times"], intRes["ys"][1, :], color=colorNeuron1, 
                              label=r"$\varphi_1$")
    plt.xlabel("Time (sec)")
    plt.ylabel("Phase Deviation")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend(loc="upper left")

    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

