
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    epsilon = 0.01
    i0 = 35
    couplingStartTime = 100.44
    colorNeuron0 = "blue"
    colorNeuron1 = "green"
    linestyleCoupled = "-"
    linestyleUncoupled = ":"
    integrationWCOsFilename = "results/integrationWCoupledINapIKLowThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    integrationPhaseDiffsFilename = "results/integrationPhasesDifferencesINapIKLowThresholdI0%.02fEpsilon%.05fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)

    integrationWCOs = np.load(integrationWCOsFilename)
    integrationPhaseDiffs = np.load(integrationPhaseDiffsFilename)

    ax1= plt.subplot(2, 1, 1)
    plt.plot(integrationWCOs["timesCoupled"],
              integrationWCOs["ysCoupled"][0,:], color=colorNeuron0,
              linestyle=linestyleCoupled, label=r"coupled $V_0$")
    plt.plot(integrationWCOs["timesCoupled"],
              integrationWCOs["ysCoupled"][2,:], color=colorNeuron1,
              linestyle=linestyleCoupled, label=r"coupled $V_1$")
    plt.plot(integrationWCOs["times0Uncoupled"],
              integrationWCOs["ys0Uncoupled"][0,:], color=colorNeuron0,
              linestyle=linestyleUncoupled, label=r"uncoupled $V_0$")
    plt.plot(integrationWCOs["times1Uncoupled"], 
              integrationWCOs["ys1Uncoupled"][0,:], color=colorNeuron1,
              linestyle=linestyleUncoupled, label=r"uncoupled $V_1$")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane\nPotential (mV)")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend(loc="upper right")

    ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    plt.plot(integrationPhaseDiffs["times"], integrationPhaseDiffs["ys"][0, :], color=colorNeuron0, label=r"$\varphi_0$")
    plt.plot(integrationPhaseDiffs["times"], integrationPhaseDiffs["ys"][1, :], color=colorNeuron1, label=r"$\varphi_1$")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Phase Deviation")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend(loc="upper right")

    plt.show()

    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

