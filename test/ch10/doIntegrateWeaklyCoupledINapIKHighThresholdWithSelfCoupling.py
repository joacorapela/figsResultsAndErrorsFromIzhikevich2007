
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
    epsilon = 0.1
    v00 =  10.00 # blue
    n00 = 0.17   # blue
    v01 = -68.00 # red
    n01 = 0.047  # red
    t0 = 0.0
    tf = 500.0
    dt = 1e-3
    couplingStartTime = 99.04
    selfCouplingStrength = 0.3
    nTSteps = int((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    i0 = 10
    traceColNeuron1 = "blue"
    traceColNeuron2 = "red"
    linestyleCoupled = "-"
    linestyleUncoupled = ":"
    resultsFilename = "results/integrationWCoupledINapIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02f.npz"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    voltagesFigFilename = "figures/voltagesWCoupledINIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02f.eps"%(selfCouplingStrength, i0, epsilon, couplingStartTime)
    phaseSpaceFigFilename = "figures/phaseSpaceWCoupledINIKHighThresholdWithSelfCouplingStrength%.02fI0%.02fEpsilon%.06fCouplingStartTime%.02f.eps"%(selfCouplingStrength, i0, epsilon, couplingStartTime)

    def i(t):
        return(i0)
    iNapIKModel1 = INapIKModel.getHighThresholdInstance()
    iNapIKModel1.setI(i=i)
    iNapIKModel2 = INapIKModel.getHighThresholdInstance()
    iNapIKModel2.setI(i=i)

    models = [iNapIKModel1, iNapIKModel2]

    # g_{ij}(x_i, x_j) is the coupling from neuron j to neuron i In
    # couplingFunc(x1, x2) x1==x_i (i.e., the state of the neuron receiving
    # the coupling) and x2=x_j (i.e., the state of the neuron sending the
    # coupling)

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

    plt.plot(timesCoupled, ysCoupled[0, :], 
                           color=traceColNeuron1, 
                           linestyle=linestyleCoupled,
                           label="Coupled Neuron 1")
    plt.plot(timesCoupled, ysCoupled[2, :], 
                           color=traceColNeuron2,
                           linestyle=linestyleCoupled,
                           label="Coupled Neuron 2")
    plt.plot(times0Uncoupled, ys0Uncoupled[0, :], 
                              color=traceColNeuron1, 
                              linestyle=linestyleUncoupled,
                              label="Uncoupled Neuron 1")
    plt.plot(times1Uncoupled, ys1Uncoupled[0, :], 
                              color=traceColNeuron2, 
                              linestyle=linestyleUncoupled,
                              label="Uncoupled Neuron 2")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("membrane potential (mV)")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend()
    plt.savefig(voltagesFigFilename)

    plt.figure()
    plt.plot(ysCoupled[0, :], ysCoupled[1, :], 
                              color=traceColNeuron1, 
                              linestyle=linestyleCoupled,
                              label="Coupled Neuron 0")
    plt.plot(ysCoupled[2, :], ysCoupled[3, :], 
                              color=traceColNeuron2, 
                              linestyle=linestyleCoupled,
                              label="Coupled Neuron 1")
    plt.plot(ys0Uncoupled[0, :], ys0Uncoupled[1, :], 
                                 color=traceColNeuron1, 
                                 linestyle=linestyleUncoupled,
                                 label="Uncoupled Neuron 0")
    plt.plot(ys1Uncoupled[0, :], ys1Uncoupled[1, :], 
                                 color=traceColNeuron2, 
                                 linestyle=linestyleUncoupled,
                                 label="Uncoupled Neuron 1")
    plt.grid()
    plt.ylabel("membrane potential (mV)")
    plt.ylabel("activation gate, n")
    plt.legend()
    plt.savefig(phaseSpaceFigFilename)

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

