
import sys
import numpy as np
import pdb
import matplotlib.pyplot as plt
from scipy.integrate import ode
from INapIKModel import INapIKModel
from WeaklyCoupledOscillatorsModel import WeaklyCoupledOscillatorsModel
from utils import integrateModelForward

def main(argv):
    epsilon = 0.033
    # epsilon = 0.00
    v01 =  10.00 # blue
    n01 = 0.17   # blue
    v02 = -68.00 # red
    n02 = 0.047  # red
    t0 = 0.0
    tf = 50.0
    dt = 1e-3
    nTSteps = int((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    i0 = 10
    traceCol1 = "blue"
    traceCol2 = "red"
    resultsFilename = "results/integrationWCoupledINapIKI0%.02fEpsilon%.02f.npz"%(i0, epsilon)
    voltagesFigFilename = "figures/voltagesWCoupledINIKI0%.02fEpsilong%.02f.eps"%(i0, epsilon)
    phaseSpaceFigFilename = "figures/phaseSpaceWCoupledINIKI0%.02fEpsilong%.02f.eps"%(i0, epsilon)

    def i(t):
        return(i0)
    iNapIKModel1 = INapIKModel.getHighThresholdInstance()
    iNapIKModel1.setI(i=i)
    iNapIKModel2 = INapIKModel.getHighThresholdInstance()
    iNapIKModel2.setI(i=i)

    models = [iNapIKModel1, iNapIKModel2]
    coupling11 = lambda x1, x2: 0.0
    coupling12 = lambda x1, x2: x2-x1
    coupling21 = lambda x1, x2: x2-x1
    coupling22 = lambda x1, x2: 0.0
    couplings = [[coupling11, coupling12], [coupling21, coupling22]]

    oscillatorsModel = WeaklyCoupledOscillatorsModel(models=models, 
                                                      couplings=couplings, 
                                                      epsilon=epsilon)
    # n01 = iNapIKModel1._nInf(v=v01)
    # n02 = iNapIKModel2._nInf(v=v02)
    y0 = np.array([v01, n01, v02, n02])
    res = integrateModelForward(model=oscillatorsModel, y0=y0, dt=dt, 
                                                        nTSteps=nTSteps)
    ys = res["ys"]
    times = res["times"]
    np.savez(resultsFilename, times=times, ys=ys)

    plt.plot(times, ys[0, :], color=traceCol1)
    plt.plot(times, ys[2, :], color=traceCol2)
    plt.grid()
    plt.xlabel("Time (sec)")
    plt.ylabel("membrane potential (mV)")
    plt.savefig(voltagesFigFilename)

    plt.figure()
    plt.plot(ys[0, :], ys[1, :], color=traceCol1)
    plt.plot(ys[2, :], ys[3, :], color=traceCol2)
    plt.grid()
    plt.ylabel("membrane potential (mV)")
    plt.ylabel("activation gate, n")
    plt.savefig(phaseSpaceFigFilename)

    plt.show()
    pdb.set_trace()

if __name__ == "__main__":
    main(sys.argv)

