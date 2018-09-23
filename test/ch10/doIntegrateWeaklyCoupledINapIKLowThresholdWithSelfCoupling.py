
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
    v00 = -26.30 # red
    n00 = 0.50   # red
    v01 = -65.01 # blue
    n01 = 0.16   # blue
    # set 2
    # v00 = -70.41 # red
    # n00 = 0.46   # red
    # v01 = -65.01 # blue
    # n01 = 0.16   # blue
    # set 3
    # v00 = -67.42 # red
    # n00 = 0.20   # red
    # v01 = -65.01 # blue
    # n01 = 0.16   # blue
    t0 = 0.0
    tf = 1500.0
    # tf = 4.0
    dt = 1e-3
    nTSteps = int((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    traceColNeuron1 = "blue"
    traceColNeuron2 = "red"
    linestyleCoupled = "-"
    linestyleUncoupled = ":"
    resultsFilename = "results/integrationWCoupledINapIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02fV00%.02fN00%.02fV01%.02fN01%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime, v00, n00, v01, n01)
    # voltagesFigFilename = "figures/voltagesWCoupledINIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02fV00%.02fN00%.02fV01%.02fN01%.02f.eps"%(selfCouplingStrength, i0, epsilon, couplingStartTime, v00, n00, v01, n01)
    phaseSpaceFigFilenamePattern = "figures/phaseSpaceNeuron%dWCoupledINIKLowThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02fV00%.02fN00%.02f.eps"
    phaseSpaceNeuron0FigFilename = phaseSpaceFigFilenamePattern%(0, selfCouplingStrength, i0, epsilon, couplingStartTime, v00, n00)
    phaseSpaceNeuron1FigFilename = phaseSpaceFigFilenamePattern%(1, selfCouplingStrength, i0, epsilon, couplingStartTime, v01, n01)

    def i(t):
        return(i0)
    iNapIKModel1 = INapIKModel.getLowThresholdInstance()
    iNapIKModel1.setI(i=i)
    iNapIKModel2 = INapIKModel.getLowThresholdInstance()
    iNapIKModel2.setI(i=i)

    models = [iNapIKModel1, iNapIKModel2] 

    # g_{ij}(x_i, x_j) is the coupling from neuron j to neuron i.

    #  In coupledFunc(x1, x2) x1==x_i (i.e., the state of the neuron
    #  receiving the coupling) and x2=x_j (i.e., the state of the neuron
    #  sending the coupling)

    uncoupledFunc = lambda x1, x2: np.array([0.0, 0.0])
    btwCoupledFunc = lambda x1, x2: np.array([x2[0]-x1[0], 0.0]) 
    selfCoupledFunc = lambda x1, x2: np.array([selfCouplingStrength*x1[0], 0.0])
    couplings = [[selfCoupledFunc, btwCoupledFunc], 
                 [btwCoupledFunc, uncoupledFunc]]

    y0 = np.array([v00, n00, v01, n01])

    coupledOscillatorsModel = WeaklyCoupledOscillatorsModel(models=models, 
                                                             couplings=
                                                              couplings, 
                                                             epsilon=epsilon,
                                                             couplingStartTime=
                                                              couplingStartTime)
    res = integrateForward(deriv=coupledOscillatorsModel.deriv, t0=t0, y0=y0, dt=dt, 
                                                               nTSteps=nTSteps)
    ysCoupled = res["ys"]
    timesCoupled= res["times"]

    y00 = np.array([v00, n00])
    res = integrateForward(deriv=iNapIKModel1.deriv, t0=t0, y0=y00, dt=dt,
                                                    nTSteps=nTSteps)
    ys0Uncoupled = res["ys"]
    times0Uncoupled= res["times"]

    y01 = np.array([v01, n01])
    res = integrateForward(deriv=iNapIKModel2.deriv, t0=t0, y0=y01, dt=dt,
                                                    nTSteps=nTSteps)
    ys1Uncoupled = res["ys"]
    times1Uncoupled= res["times"]

    np.savez(resultsFilename, timesCoupled=timesCoupled, 
                              ysCoupled=ysCoupled,
                              times0Uncoupled=times0Uncoupled,
                              ys0Uncoupled=ys0Uncoupled,
                              times1Uncoupled=times1Uncoupled,
                              ys1Uncoupled=ys1Uncoupled)

    plt.plot(ysCoupled[0, :], ysCoupled[1, :], 
                              color=traceColCoupled, 
                              linestyle=linestyleCoupled,
                              label="Coupled")
    plt.plot(ys0Uncoupled[0, :], ys0Uncoupled[1, :], 
                                 color=traceColNeuron1, 
                                 linestyle=linestyleUncoupled,
                                 label="Uncoupled")
    plt.grid()
    plt.ylabel("membrane potential (mV)")
    plt.ylabel("activation gate, n")
    plt.legend()
    plt.savefig(phaseSpaceNeuron0FigFilename)


    plt.plot(ysCoupled[2, :], ysCoupled[3, :], 
                              color=traceColCoupled, 
                              linestyle=linestyleCoupled,
                              label="Coupled Neuron 1")
    plt.plot(ys1Uncoupled[0, :], ys1Uncoupled[1, :], 
                                 color=traceColUncoupled, 
                                 linestyle=linestyleUncoupled,
                                 label="Uncoupled Neuron 1")
    plt.grid()
    plt.ylabel("membrane potential (mV)")
    plt.ylabel("activation gate, n")
    plt.legend()
    plt.savefig(phaseSpaceNeuron1FigFilename)

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

