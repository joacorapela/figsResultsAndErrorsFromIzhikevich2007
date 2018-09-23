
import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel
from WeaklyCoupledOscillatorsModel import WeaklyCoupledOscillatorsModel
from utils import integrateForward

def main(argv):
    if len(argv)!=2:
        print("Usage: %s <selfCouplingStrength>"%argv[0])
        sys.exit(1)

    selfCouplingStrength = float(argv[1])
    epsilon = 0.003
    couplingStartTime = 100.44
    i0 = 35.0
    # set 1
    # v00 = -26.30 # red
    # n00 = 0.50   # red
    # v01 = -65.01 # blue
    # n01 = 0.16   # blue
    # set 2
    # v00 = -70.41 # red
    # n00 = 0.46   # red
    # v01 = -65.01 # blue
    # n01 = 0.16   # blue
    # set 3
    v00 = -67.42 # red
    n00 = 0.20   # red
    v01 = -65.01 # blue
    n01 = 0.16   # blue
    traceColCoupled = "blue"
    traceColUncoupled = "red"
    linestyleCoupled = "-"
    linestyleUncoupled = "-"
    ylim = [.1, .7]
    resultsFilename = "results/integrationWCoupledINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02fV00%.02fN00%.02fV01%.02fN01%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime, v00, n00, v01, n01)
    phaseSpaceFigFilenamePattern = "figures/phaseSpaceNeuron%dWCoupledINIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02fV00%.02fN00%.02f.eps"

    phaseSpaceNeuron0FigFilename = phaseSpaceFigFilenamePattern%(0, selfCouplingStrength, i0, epsilon, couplingStartTime, v00, n00)
    phaseSpaceNeuron1FigFilename = phaseSpaceFigFilenamePattern%(1, selfCouplingStrength, i0, epsilon, couplingStartTime, v01, n01)

    results = np.load(resultsFilename)
    timesCoupled = results['timesCoupled']
    ysCoupled = results['ysCoupled']
    times0Uncoupled = results['times0Uncoupled']
    ys0Uncoupled = results['ys0Uncoupled']
    times1Uncoupled = results['times1Uncoupled']
    ys1Uncoupled = results['ys1Uncoupled']

    plt.plot(ysCoupled[0, :], ysCoupled[1, :], 
                              color=traceColCoupled, 
                              linestyle=linestyleCoupled,
                              label="Coupled")
    plt.plot(ys0Uncoupled[0, :], ys0Uncoupled[1, :], 
                                 color=traceColUncoupled, 
                                 linestyle=linestyleUncoupled,
                                 label="Uncoupled")
    plt.ylim(ylim)
    plt.grid()
    plt.xlabel("membrane potential (mV)")
    plt.ylabel("activation gate, n")
    plt.legend()
    plt.savefig(phaseSpaceNeuron0FigFilename)

    plt.figure()
    plt.plot(ysCoupled[2, :], ysCoupled[3, :], 
                              color=traceColCoupled, 
                              linestyle=linestyleCoupled,
                              label="Coupled")
    plt.plot(ys1Uncoupled[0, :], ys1Uncoupled[1, :], 
                                 color=traceColUncoupled, 
                                 linestyle=linestyleUncoupled,
                                 label="Uncoupled")
    plt.ylim(ylim)
    plt.grid()
    plt.xlabel("membrane potential (mV)")
    plt.ylabel("activation gate, n")
    plt.legend()
    plt.savefig(phaseSpaceNeuron1FigFilename)

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

