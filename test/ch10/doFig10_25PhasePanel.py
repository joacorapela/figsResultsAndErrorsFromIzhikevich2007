
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from syncUtils import getPhasesFromVoltages

def main(argv):
    epsilon = 5.0*1e-4
    i0 = 10
    couplingStartTime = 20.0
    integrationFilename = "results/integrationWCoupledINapIKI0%.02fEpsilon%.02fCouplingStart%.02f.npz"%(i0, epsilon, couplingStartTime)
    figFilename = "results/phasesWCoupledINapIKI0%.02fEpsilon%.02fCouplingStart%.02f.eps"%(i0, epsilon, couplingStartTime)

    res = np.load(integrationFilename)
    times = res["times"]
    voltagesNeuron1 = res["ys"][0,:]
    voltagesNeuron2 = res["ys"][2,:]
    voltagesUncoupled = res["ysUncoupled"][0,:]
    timesUncoupled = res["timesUncoupled"]
    sampleRate = 1.0/(times[1]-times[0])

    phasesNeuron1 = getPhasesFromVoltages(voltages=voltagesNeuron1, sampleRate=sampleRate)
    phasesNeuron2 = getPhasesFromVoltages(voltages=voltagesNeuron2, sampleRate=sampleRate)
    phasesUncoupled = getPhasesFromVoltages(voltages=voltagesUncoupled, sampleRate=sampleRate)
    plt.plot(times, phasesNeuron1, label="Neuron 1")
    plt.plot(times, phasesNeuron2, label="Neuron 2")
    plt.plot(timesUncoupled, phasesUncoupled, label="Uncoupled Neuron 1")
    plt.legend()
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Phase (sec)")
    plt.savefig(figFilename)

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

