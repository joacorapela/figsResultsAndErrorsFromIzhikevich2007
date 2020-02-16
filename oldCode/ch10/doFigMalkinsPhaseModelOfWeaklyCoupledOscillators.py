
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(argv):
    i0 = 10
    epsilon = 2.5*1e-4
    couplingStartTime = 100.0
    dt = 1e-3
    integrationWCOsFilename = "results/integrationWCoupledINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    integrationQsFilename = "results/integrationQINapIKHighThresholdI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    integrationPhasesFilename = "results/integrationPhasesINapIKHighThresholdI0%.02fEpsilon%.05fCouplingStartTime%.02f.npz"%(i0, epsilon, couplingStartTime)
    integrationPhasesFigFilename = "figures/integrationPhasesINapIKHighThresholdI0%.02fEpsilon%.05fCouplingStartTime%.02f.eps"%(i0, epsilon, couplingStartTime)

    integrationWCOs = np.load(integrationWCOsFilename)
    qsIntRes = np.load(integrationQsFilename)
    integrationPhases = np.load(integrationPhasesFilename)

    ax1 = plt.subplot(211)
    plt.plot(integrationWCOs["times"], integrationWCOs["ys"][0,:], 
                                       color="red", label=r"$V_1$")
    plt.plot(integrationWCOs["times"], integrationWCOs["ys"][2,:],
                                       color="blue", label=r"$V_2$")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane\nPotential (mV)")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend(loc="upper left")

    T = np.max(qsIntRes["times"])
    ax2= plt.subplot(212, sharex=ax1)
    plt.plot(integrationPhases["times"], integrationPhases["ys"][0, :]%T,
                                         color="red", label=r"$\theta_1$")
    plt.plot(integrationPhases["times"], integrationPhases["ys"][1, :]%T,
                                         color="blue", label=r"$\theta_2$")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Phase")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend(loc="upper left")

    plt.savefig(integrationPhasesFigFilename)
    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

