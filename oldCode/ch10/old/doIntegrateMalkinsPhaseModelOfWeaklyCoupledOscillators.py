
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from MalkinsPhaseModelOfWeaklyCoupledOscillators import MalkinsPhaseModelOfWeaklyCoupledOscillators 
from utils import integrateForward
from syncUtils import getPhasesFromVoltages

def main(argv):
    i0 = 10
    epsilon = 2.5*1e-4
    couplingStartTime = 100.0
    dt = 1e-3
    integrationWCOsFilename = "results/integrationWCoupledINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    integrationQsFilename = "results/integrationQINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    resultsFilename = "results/integrationPhasesINapIKHighThresholdI0%.02fEpsilon%.05fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)

    integrationWCOs = np.load(integrationWCOsFilename)
    qsIntRes = np.load(integrationQsFilename)
    T = np.max(qsIntRes["times"])
    def Q(phase, qIndex):
        wrappedPhase = phase%T
        phaseIndex = np.argmin(np.abs(wrappedPhase-qsIntRes["times"]))
        answer = qsIntRes["ys"][qIndex, phaseIndex]
        print("Q%d[phase=%.04f]=%.04f"%(qIndex, wrappedPhase, answer))
        return(answer)

    Q1 = lambda phase: Q(phase, 0)
    Q2 = lambda phase: Q(phase, 1)
    qs = [Q1, Q2]

    uncoupledFunc = lambda x1, x2: 0.0
    coupledFunc = lambda x1, x2: x1[0]-x2[0]
    couplings_V = [[uncoupledFunc, coupledFunc], 
                   [coupledFunc, uncoupledFunc]]
    couplings_n = [[uncoupledFunc, uncoupledFunc], 
                   [uncoupledFunc, uncoupledFunc]]
    couplings = [couplings_V, couplings_n]

    malkinsPhaseModel = \
     MalkinsPhaseModelOfWeaklyCoupledOscillators(xs=integrationWCOs["ys"], 
                                                  xsTimes=
                                                   integrationWCOs["times"],
                                                  qs=qs, couplings=couplings, 
                                                  # epsilon=epsilon,
                                                  epsilon=epsilon*1e3,
                                                  couplingStartTime=
                                                   couplingStartTime)

    times = integrationWCOs["times"]
    voltagesNeuron1 = integrationWCOs["ys"][0,:]
    voltagesNeuron2 = integrationWCOs["ys"][2,:]

    resPhasesNeuron1 = getPhasesFromVoltages(times=times, 
                                              voltages=voltagesNeuron1)
    phasesNeuron1 = resPhasesNeuron1["phases"]
    timePhasesNeuron1 = resPhasesNeuron1["times"]
    resPhasesNeuron2 = getPhasesFromVoltages(times=times,
                                              voltages=voltagesNeuron2)
    phasesNeuron2 = resPhasesNeuron2["phases"]
    timePhasesNeuron2 = resPhasesNeuron2["times"]

    if timePhasesNeuron1[0]<=timePhasesNeuron2[0]:
        indexT0Neuron2 = 0
        indexT0Neuron1 = np.argmin(np.abs(timePhasesNeuron2[0]-timePhasesNeuron1))
    else:
        indexT0Neuron1 = 0
        indexT0Neuron2 = np.argmin(np.abs(timePhasesNeuron1[0]-timePhasesNeuron2))
    phase0Neuron1 = phasesNeuron1[indexT0Neuron1]
    phase0Neuron2 = phasesNeuron2[indexT0Neuron2]
    y0 = [phase0Neuron1, phase0Neuron2]
    t0 = timePhasesNeuron1[indexT0Neuron1]

    if timePhasesNeuron1[-1]<=timePhasesNeuron2[-1]:
        indexTfNeuron1 = -1
        indexTfNeuron2 = np.argmin(np.abs(timePhasesNeuron1[-1]-timePhasesNeuron2))
    else:
        indexTfNeuron2 = -1
        indexTfNeuron1 = np.argmin(np.abs(timePhasesNeuron2[-1]-timePhasesNeuron1))
    tf = timePhasesNeuron1[indexTfNeuron1]
    nTSteps = int((tf-t0)/dt)

    intRes = integrateForward(deriv=malkinsPhaseModel.deriv, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
    np.savez(resultsFilename, times=intRes["times"], ys=intRes["ys"])

    ax1= plt.subplot(2, 1, 1)
    plt.plot(integrationWCOs["times"], integrationWCOs["ys"][0,:], color="red", label=r"$V_1$")
    plt.plot(integrationWCOs["times"], integrationWCOs["ys"][2,:], color="blue", label=r"$V_2$")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane\nPotential (mV)")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend(loc="upper left")

    ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    plt.plot(intRes["times"], intRes["ys"][0, :]%T, color="red", label=r"$\theta_1$")
    plt.plot(intRes["times"], intRes["ys"][1, :]%T, color="blue", label=r"$\theta_2$")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Phase")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend(loc="upper left")

    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

