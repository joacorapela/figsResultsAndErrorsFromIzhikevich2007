
import sys
import numpy as np
import pdb
# from scipy.integrate import ode
# from scipy.integrate import odeint
import matplotlib.pyplot as plt
from INapIKModel import INapIKModel
from utils import integrateForward, integrateBackward
from plotFunctions import plotHighThresholdINapIKVectorField

def main(argv):
    def integrateForwardManually(deriv, t0, y0, dt, nTSteps):
        ts = np.empty(nTSteps)
        ys = np.empty((len(y0), nTSteps))
        t = t0
        y = y0
        ts[0] = t
        ys[:,0] = y
        for i in range(1,nTSteps):
            t = t+dt
            y = y+dt*deriv(y=y, t=t)
            print("t=%.02f, V=%.02f, n=%.02f"% (t, y[0], y[1]))
            ts[i] = t
            ys[:,i] = y
        return {"times":ts, "ys":ys}

    def integrateBackwardManually(deriv, t0, y0, dt, nTSteps):
        ts = np.empty(nTSteps)
        ys = np.empty((len(y0), nTSteps))
        t = t0
        y = y0
        ts[0] = t
        ys[:,0] = y
        for i in range(1,nTSteps):
            t = t-dt
            y = y+dt*deriv(y=y, t=t)
            if y[1]<0.0:
                y[1] = 0.0
            print("t=%.02f, V=%.02f, n=%.02f"% (t, y[0], y[1]))
            ts[i] = t
            ys[:,i] = y
        return {"times":ts, "ys":ys}

    epsilon = 1e-6
    # v0 = 10.00
    v0 = -61.0
    n0 = 0.48110
    t0 = 0.0
    # tf = 1*7.25
    tf = 1*7.25
    dt = 1e-3
    nTSteps = int(round((tf-t0)/dt))
    i0 = 10
    def i(t):
        return(i0)
    iNapIKModel = INapIKModel.getHighThresholdInstance()
    iNapIKModel.setI(i=i)
    # n0 = iNapIKModel._nInf(v=v0)

    y0 = np.array([v0, n0])
    # res = integrateForward(deriv=iNapIKModel.deriv, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
    res = integrateBackward(deriv=iNapIKModel.deriv, t0=tf, y0=y0, dt=dt, nTSteps=nTSteps)
    # res = integrateForwardManually(deriv=iNapIKModel.deriv, t0=t0, y0=y0, dt=dt, nTSteps=nTSteps)
    # res = integrateBackwardManually(deriv=iNapIKModel.deriv, t0=tf, y0=y0, dt=dt, nTSteps=nTSteps)
    plt.plot(res["times"], res["ys"][0,:])
    plt.xlabel("Time (sec)")
    plt.ylabel("Voltage (mV)")
    plt.ylim((-100,20))

    plt.figure()
    plotHighThresholdINapIKVectorField(i=i0)
    plt.plot(res["ys"][0, :], res["ys"][1, :], label="limit cycle attractor")
    plt.xlim((-100, 20))
    plt.xlabel('Voltage (mv)')
    plt.ylabel('K activation variable, n')

    plt.show()
    pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

