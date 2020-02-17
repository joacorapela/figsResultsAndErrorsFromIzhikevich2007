
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel
from WeaklyCoupledOscillatorsModel import WeaklyCoupledOscillatorsModel
from utils import integrateModelForward

def main(argv):
    epsilon = 2.5*1e-4
    # epsilon = 0.00
    v01 =  10.00 # blue
    n01 = 0.17   # blue
    v02 = -68.00 # red
    n02 = 0.047  # red
    v03 = -37.00 # red
    n03 = 0.55  # red
    t0 = 0.0
    tf = 500.0
    dt = 1e-3
    couplingStartTime = 100.0
    nTSteps = int((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    i0 = 10
    traceCol1 = "red"
    traceCol2 = "green"
    traceCol3 = "blue"
    resultsFilename = "results/integrationWCoupledINapIKI0%.02fEpsilon%.02fCouplingStart%.02f_myGame.npz"%(i0, epsilon, couplingStartTime)
    voltagesFigFilename = "figures/voltagesWCoupledINIKI0%.02fEpsilong%.02fCouplingStart%.02f_myGame.eps"%(i0, epsilon, couplingStartTime)
    phaseSpaceFigFilename = "figures/phaseSpaceWCoupledINIKI0%.02fEpsilong%.02fCouplingStart%.02f_myGame.eps"%(i0, epsilon, couplingStartTime)

    def i(t):
        return(i0)
    iNapIKModel1 = INapIKModel.getHighThresholdInstance()
    iNapIKModel1.setI(i=i)
    iNapIKModel2 = INapIKModel.getHighThresholdInstance()
    iNapIKModel2.setI(i=i)
    iNapIKModel3 = INapIKModel.getHighThresholdInstance()
    iNapIKModel3.setI(i=i)

    coupleConstantForPhaseDelay = 20
    models = [iNapIKModel1, iNapIKModel2, iNapIKModel3]
    uncoupledFunc = lambda x1, x2: 0.0
    coupledFunc = lambda x1, x2: x1[0]-x2[0]+coupleConstantForPhaseDelay
    couplings = [[uncoupledFunc, uncoupledFunc, uncoupledFunc], 
                 [coupledFunc, uncoupledFunc, uncoupledFunc],
                 [uncoupledFunc, coupledFunc, uncoupledFunc]]

    y0 = np.array([v01, n01, v02, n02, v03, n03])

    coupledOscillatorsModel = WeaklyCoupledOscillatorsModel(models=models, 
                                                             couplings=couplings, 
                                                             epsilon=epsilon,
                                                             couplingStartTime=
                                                              couplingStartTime)
    res = integrateModelForward(model=coupledOscillatorsModel, y0=y0, dt=dt, 
                                                               nTSteps=nTSteps)
    ys = res["ys"]
    times= res["times"]

    np.savez(resultsFilename, times=times, 
                              ys=ys)

    plt.plot(times, ys[0, :], color=traceCol1, label="Neuron 1")
    plt.plot(times, ys[2, :], color=traceCol2, label="Neuron 2")
    plt.plot(times, ys[4, :], color=traceCol3, label="Neuron 3")
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane potential (mV)")
    plt.axvline(x=couplingStartTime, color="red")
    plt.legend()
    plt.savefig(voltagesFigFilename)

    plt.figure()
    plt.plot(ys[0, :], ys[1, :], color=traceCol1, label="Neuron 1")
    plt.plot(ys[2, :], ys[3, :], color=traceCol2, label="Neuron 2")
    plt.plot(ys[4, :], ys[5, :], color=traceCol3, label="Neuron 3")
    plt.grid()
    plt.xlabel("Membrane potential (mV)")
    plt.ylabel("Activation gate, n")
    plt.legend()
    plt.savefig(phaseSpaceFigFilename)

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

