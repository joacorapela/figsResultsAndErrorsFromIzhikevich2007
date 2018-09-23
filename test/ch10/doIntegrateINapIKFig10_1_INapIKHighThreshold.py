
import sys
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateForward

def main(argv):
    resultsFilename = 'results/integrationINapIKFig10_1_INapIKHighThreshold.npz'
    v0 = -60.00
    t0 = 0.0
    tf = 25.0
    dt = 1e-5
    nTSteps = round((tf-t0)/dt)
    times = np.empty(nTSteps+1)
    i0 = 10
    def i(t):
        return(i0)
    iNapIKModel = INapIKModel.getHighThresholdInstance()
    iNapIKModel.setI(i=i)
    n0 = iNapIKModel._nInf(v=v0)
    y0 = np.array([v0, n0])
    res = integrateForward(deriv=iNapIKModel.deriv, t0=t0, y0=y0, dt=dt, 
                                                    nTSteps=nTSteps)
    np.savez(resultsFilename, times=res['times'], ys=res['ys'])

    plt.plot(res['times'], res['ys'][0,:])
    plt.xlabel("Time (sec)")
    plt.ylabel("Membrane Potential (mV)")
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

